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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://finance.yahoo.com/"
    }

    print(f"正在查詢股票: {stockNumber}.TW，URL: {url}")  # 添加日誌

    try:
        response = requests.get(url, headers=headers, timeout=10)  # 添加超時設定
        response.raise_for_status()  # 如果請求失敗，拋出異常
        data = response.json()

        print(f"API 回應: {data}")  # 打印回應以調試

        if "quoteResponse" in data and "result" in data["quoteResponse"]:
            stock_info = data["quoteResponse"]["result"]
            if stock_info and len(stock_info) > 0:
                return stock_info[0].get("shortName", "no")
            else:
                print("無效的股票資訊")
                return "no"
        else:
            print("API 回應格式錯誤")
            return "no"

    except requests.exceptions.RequestException as e:
        print(f"網絡請求失敗: {e}")
        return "no"
    except json.JSONDecodeError as e:
        print(f"JSON 解析失敗: {e}")
        return "no"
    except Exception as e:
        print(f"其他錯誤: {e}")
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
    stock = yf.Ticker(stockNumber + ".TW")
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)  # 設定一年內的資料
    stock_data = stock.history(start=start, end=end)

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data["Close"], '-', label="收盤價")
    plt.plot(stock_data["High"], '-', label="最高價")
    plt.plot(stock_data["Low"], '-', label="最低價")
    plt.title(stockNumber + ' 收盤價年走勢', loc='center', fontsize=20, fontproperties=font_path)
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('價格', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=font_path)
    plt.savefig(msg + '.png')  # 存檔
    plt.show()
    plt.close() 
    return Imgur.showImgur(msg)

# --------- 股票收益率: 代表股票在一天交易中的價值變化百分比
def show_return(stockNumber, msg):
    stock = yf.Ticker(stockNumber + ".TW")
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)  # 設定一年內的資料
    stock_data = stock.history(start=start, end=end)

    stock_data['Returns'] = stock_data['Close'].pct_change()
    stock_return = stock_data['Returns'].dropna()

    plt.figure(figsize=(12, 6))
    plt.plot(stock_return, label="報酬率")
    plt.title(stockNumber + ' 年收益率走勢', loc='center', fontsize=20, fontproperties=font_path)
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('報酬率', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=font_path)
    plt.savefig(msg + '.png')  # 存檔
    plt.show()
    plt.close()
    return Imgur.showImgur(msg)

# --------- 畫股價震盪圖
def show_fluctuation(stockNumber, msg):
    stock = yf.Ticker(stockNumber + ".TW")
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)  # 設定一年內的資料
    stock_data = stock.history(start=start, end=end)

    stock_data['stock_fluctuation'] = stock_data["High"] - stock_data["Low"]

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data['stock_fluctuation'], '-', label="波動度", color="orange")
    plt.title(stockNumber + ' 收盤價年波動度', loc='center', fontsize=20, fontproperties=font_path)
    plt.xlabel('日期', fontsize=20, fontproperties=font_path)
    plt.ylabel('價格', fontsize=20, fontproperties=font_path)
    plt.grid(True, axis='y')
    plt.legend(fontsize=14, prop=font_path)
    plt.savefig(msg + '.png')  # 存檔
    plt.show()
    plt.close()
    return Imgur.showImgur(msg)
