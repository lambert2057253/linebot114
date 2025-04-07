# Technical_Analysis.py
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import yfinance as yf
import requests
import datetime
from bs4 import BeautifulSoup
from matplotlib.font_manager import FontProperties
import os

# 固定字體路徑
font_path = '/opt/render/project/src/msjh.ttf'
if not os.path.exists(font_path):
    print(f"[log:ERROR] Font file {font_path} not found! Using default font.")
    chinese_font = FontProperties()
else:
    print(f"[log:INFO] Font file {font_path} found.")
    chinese_font = FontProperties(fname=font_path)

def general_df(stockNumber):
    stockNumberTW = stockNumber + ".TW"
    df_x = pdr.DataReader(stockNumberTW, 'yahoo', start="2019")
    df_x.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}, inplace=True)
    return df_x

def get_stockName(stockNumber):
    try:
        # 使用 yfinance 獲取股票名稱
        stock = yf.Ticker(stockNumber + '.TW')
        info = stock.info
        stock_name = info.get('longName', stockNumber)  # 若無名稱，返回代碼
        return stock_name
    except Exception as e:
        print(f"[log:ERROR] Failed to get stock name from yfinance: {e}")
        # 備用方法：從網頁獲取
        try:
            url = f'https://tw.stock.yahoo.com/q/q?s={stockNumber}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all(text='成交')[0].parent.parent.parent
            trs = table.select('tr')
            if len(trs) > 1:
                stock_name = trs[1].select('td')[0].text.strip('加到投資組合')
                return stock_name
            else:
                print(f"[log:ERROR] Table structure invalid for {stockNumber}")
                return stockNumber  # 若無法解析，返回代碼
        except Exception as e:
            print(f"[log:ERROR] Failed to get stock name from web: {e}")
            return stockNumber  # 最終備用，返回代碼

def MACD_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj = df_x.reset_index(drop=False)
    
    # 手動計算 MACD
    ema12 = df_x['close'].ewm(span=12, adjust=False).mean()
    ema26 = df_x['close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - signal
    macd_df = pd.DataFrame({
        'MACD': macd,
        'MACD Signal': signal,
        'MACD Hist': macd_hist
    }, index=df_x.index)
    
    macd_df.plot(figsize=(16, 8))
    plt.xlabel("日期", fontproperties=chinese_font)
    plt.ylabel("值", fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.title(stock_name + " MACD線", fontproperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgur(msg)

def RSI_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj = df_x.reset_index(drop=False)
    
    # 手動計算 RSI
    delta = df_x['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame({'RSI': rsi}, index=df_x.index)
    
    rsi_df.plot(figsize=(16, 8))
    plt.xlabel("日期", fontproperties=chinese_font)
    plt.ylabel("KD值", fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.title(stock_name + " KD線", fontproperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgur(msg)

def BBANDS_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj = df_x.reset_index(drop=False)
    
    # 手動計算 BBANDS
    sma = df_x['close'].rolling(window=20).mean()
    std = df_x['close'].rolling(window=20).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    bbands_df = pd.DataFrame({
        'Upper Band': upper_band,
        'Middle Band': sma,
        'Lower Band': lower_band
    }, index=df_x.index)
    
    bbands_df.plot(figsize=(16, 8))
    plt.xlabel("日期", fontproperties=chinese_font)
    plt.ylabel("價格", fontproperties=chinese_font)
    plt.grid(True, axis='y')
    plt.title(stock_name + " BBANDS", fontproperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgur(msg)
