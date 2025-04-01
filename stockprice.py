# -*- coding: utf-8 -*-
''' 
即時股價
'''
import requests
import datetime
import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf  # 改用 yfinance
from bs4 import BeautifulSoup
import Imgur
from matplotlib.font_manager import FontProperties # 設定字體

font_path = matplotlib.font_manager.FontProperties(fname='msjh.ttf')

emoji_upinfo = u'\U0001F447'
emoji_midinfo = u'\U0001F538'
emoji_downinfo = u'\U0001F60A'

# 使用 Yahoo Finance API 獲取股票名稱
def get_stock_name(stockNumber):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={stockNumber}.TW"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if "quoteResponse" in data and "result" in data["quoteResponse"]:
            stock_info = data["quoteResponse"]["result"]
            if stock_info:
                return stock_info[0]["shortName"]
    except Exception as e:
        print("股票名稱獲取失敗:", e)

    return "no"

# 使用者查詢股票
def getprice(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    
    content = ""
    stock = yf.Ticker(stockNumber+'.TW')
    hist = stock.history(period="7d")

    if hist.empty:
        return "查無此股票代碼或 Yahoo Finance 暫時無法提供資料!"
    
    price = hist["Close"].iloc[-1]  # 最新收盤價
    last_price = hist["Close"].iloc[-2]  # 前一天收盤價
    spread_price = price - last_price  # 價差
    spread_ratio = (spread_price / last_price) * 100  # 漲跌幅
    open_price = hist["Open"].iloc[-1]  # 開盤價
    high_price = hist["High"].iloc[-1]  # 最高價
    low_price = hist["Low"].iloc[-1]  # 最低價

    price_five = hist["Close"].tail(5)
    stockAverage = price_five.mean()
    stockSTD = price_five.std()

    spread_price = f"{'△' if spread_price > 0 else '▽'} {spread_price:.2f}"
    spread_ratio = f"{'△' if spread_price > 0 else '▽'} {spread_ratio:.2f}%"

    content += f"回報 {stock_name} ({stockNumber}) 的股價 {emoji_upinfo}\n"
    content += f"--------------\n日期: {hist.index[-1].date()}\n"
    content += f"{emoji_midinfo} 最新收盤價: {price:.2f}\n"
    content += f"{emoji_midinfo} 開盤價: {open_price:.2f}\n"
    content += f"{emoji_midinfo} 最高價: {high_price:.2f}\n"
    content += f"{emoji_midinfo} 最低價: {low_price:.2f}\n"
    content += f"{emoji_midinfo} 價差: {spread_price} 漲跌幅: {spread_ratio}\n"
    content += f"{emoji_midinfo} 近五日平均價格: {stockAverage:.2f}\n"
    content += f"{emoji_midinfo} 近五日標準差: {stockSTD:.2f}\n"
    
    if msg[0] == "#": 
        content += f"--------------\n需要更詳細的資訊，可以點選以下選項進一步查詢唷{emoji_downinfo}"
    else: 
        content += '\n' 
    
    return content

# --------- 畫近一年股價走勢圖
def stock_trend(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber+'.TW', 'yahoo', start= year+"-"+month,end=end)
    plt.figure(figsize=(12, 6))
    plt.plot(stock["Close"], '-' , label="收盤價")
    plt.plot(stock["High"], '-' , label="最高價")
    plt.plot(stock["Low"], '-' , label="最低價")
    plt.title(stock_name + '  收盤價年走勢',loc='center', fontsize=20, fontproperties=font_path)# loc->title的位置
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('價格', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=14, prop=font_path)
    plt.savefig(msg + '.png') #存檔
    plt.show()
    plt.close() 
    return Imgur.showImgur(msg)

#股票收益率: 代表股票在一天交易中的價值變化百分比
def show_return(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock['Returns'] = stock['Close'].pct_change()
    stock_return = stock['Returns'].dropna()
    plt.figure(figsize=(12, 6))
    plt.plot(stock_return, label="報酬率")
    plt.title(stock_name + '  年收益率走勢',loc='center', fontsize=20, fontproperties=font_path)# loc->title的位置
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('報酬率', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=14, prop=font_path)
    plt.savefig(msg+'.png') #存檔
    plt.show()
    return Imgur.showImgur(msg)

# --------- 畫  股價震盪圖
def show_fluctuation(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock['stock_fluctuation'] = stock["High"] - stock["Low"]
    max_value = max(stock['stock_fluctuation'][:]) # 最大價差
    min_value = min(stock['stock_fluctuation'][:]) # 最小價差
    plt.figure(figsize=(12, 6))
    plt.plot(stock['stock_fluctuation'], '-' , label="波動度", color="orange")
    plt.title(stock_name + '  收盤價年波動度',loc='center', fontsize=20, fontproperties=font_path)# loc->title的位置
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('價格', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y') # 網格線
    plt.legend(fontsize=14, prop= font_path)
    plt.savefig(msg + '.png') #存檔
    plt.show()
    plt.close() 
    return Imgur.showImgur(msg)
