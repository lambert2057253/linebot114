# -*- coding: utf-8 -*-
''' 
即時股價與走勢圖
'''
import requests
import datetime
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
import Imgur
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 設定中文字體
chinese_font = matplotlib.font_manager.FontProperties(fname='msjh.ttf') # 引入同個資料夾下支援中文字檔

# Emoji 定義
emoji_upinfo = u'\U0001F447'
emoji_midinfo = u'\U0001F538'
emoji_downinfo = u'\U0001F60A'

def get_stock_name(stockNumber):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockNumber}.TW'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        stock_name = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)').text
        return stock_name
    except Exception as e:
        print(f"[log:ERROR] Error in get_stock_name: {e}")
        return "no"

# 使用者查詢股票即時資訊
def getprice(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no":
        return "股票代碼錯誤!"
    content = ""
    stock = yf.Ticker(stockNumber + '.TW')
    hist = stock.history(period="5d")  # 獲取近5天的歷史數據
    if hist.empty:
        return "無法獲取股票數據，請確認代碼或稍後再試!"
    
    date = hist.index[-1].strftime('%Y-%m-%d')
    price = '%.2f' % hist["Close"].iloc[-1]  # 近日收盤價
    last_price = '%.2f' % hist["Close"].iloc[-2]  # 前一日收盤價
    spread_price = '%.2f' % (float(price) - float(last_price))  # 價差
    spread_ratio = '%.2f' % (float(spread_price) / float(last_price) * 100) + '%'  # 漲跌幅（百分比）
    spread_price = spread_price.replace("-", "▽ ") if float(last_price) > float(price) else "△ " + spread_price
    spread_ratio = spread_ratio.replace("-", "▽ ") if float(last_price) > float(price) else "△ " + spread_ratio
    open_price = '%.2f' % hist["Open"].iloc[-1]  # 開盤價
    high_price = '%.2f' % hist["High"].iloc[-1]  # 最高價
    low_price = '%.2f' % hist["Low"].iloc[-1]  # 最低價
    price_five = hist["Close"].iloc[-5:]  # 近五日收盤價
    stockAverage = '%.2f' % price_five.mean()  # 近五日平均價格
    stockSTD = '%.2f' % price_five.std()  # 近五日標準差
    
    content += f"{stock_name} 股票報告{emoji_upinfo}\n--------------\n日期: {date}\n{emoji_midinfo}最新收盤價: {price}\n{emoji_midinfo}開盤價: {open_price}\n{emoji_midinfo}最高價: {high_price}\n{emoji_midinfo}最低價: {low_price}\n{emoji_midinfo}漲跌價差: {spread_price} 漲跌幅: {spread_ratio}\n{emoji_midinfo}五日平均價格: {stockAverage}\n{emoji_midinfo}五日標準差: {stockSTD}\n"
    if msg.startswith("#"):
        content += f"--------------\n請選擇下方選項查看更多詳情{emoji_downinfo}"
    else:
        content += '\n'
    return content

# 畫近一年股價走勢圖
def stock_trend(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no":
        return "股票代碼錯誤!"

    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    
    stock = yf.Ticker(stockNumber + '.TW')
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)
    
    if stock_data.empty:
        print(f"[log:ERROR] No trend data for {stockNumber}.TW")
        return "no"
    
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Close"], '-', label="收盤價")
    plt.plot(stock_data["High"], '-', label="最高價")
    plt.plot(stock_data["Low"], '-', label="最低價")
    plt.title(f'{stock_name} 近一年價格走勢', loc='center', fontsize=20, fontproperties=chinese_font)
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)
    plt.ylabel('價格', fontsize=20, fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=chinese_font)
    plt.savefig(msg + '.png')
    plt.close()
    
    return Imgur.showImgur(msg)

# 股票收益率：代表股票在一天交易中的價值變化百分比
def show_return(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no":
        return "股票代碼錯誤!"

    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    
    stock = yf.Ticker(stockNumber + '.TW')
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)
    
    if stock_data.empty:
        print(f"[log:ERROR] No return data for {stockNumber}.TW")
        return "no"
    
    stock_data['Returns'] = stock_data['Close'].pct_change()
    stock_return = stock_data['Returns'].dropna()
    
    plt.figure(figsize=(12, 6))
    plt.plot(stock_return, label="收益率")
    plt.title(f'{stock_name} 近一年收益率走勢', loc='center', fontsize=20, fontproperties=chinese_font)
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)
    plt.ylabel('收益率', fontsize=20, fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=chinese_font)
    plt.savefig(msg + '.png')
    plt.close()
    
    return Imgur.showImgur(msg)

# 畫股價震盪圖
def show_fluctuation(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no":
        return "股票代碼錯誤!"

    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    
    stock = yf.Ticker(stockNumber + '.TW')
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)
    
    if stock_data.empty:
        print(f"[log:ERROR] No fluctuation data for {stockNumber}.TW")
        return "no"
    
    stock_data['stock_fluctuation'] = stock_data["High"] - stock_data["Low"]
    
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['stock_fluctuation'], '-', label="震盪幅度", color="orange")
    plt.title(f'{stock_name} 近一年價格震盪', loc='center', fontsize=20, fontproperties=chinese_font)
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)
    plt.ylabel('價格', fontsize=20, fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=chinese_font)
    plt.savefig(msg + '.png')
    plt.close()
    
    return Imgur.showImgur(msg)
