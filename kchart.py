# kchart.py
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import requests
from bs4 import BeautifulSoup
import datetime
import Imgur
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 設定全局中文字體
font_path = '/opt/render/project/src/msjh.ttf'  # 使用 Render 的絕對路徑
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = [font_path]  # 直接使用字體檔案路徑
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def get_stock_name(stockNumber):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockNumber}.TW'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        page = requests.get(url, headers=headers)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')
        stock_name = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)')
        if stock_name:
            return stock_name.text.strip()
        print(f"[log:WARNING] 找不到 {stockNumber} 的股票名稱")
        return "no"
    except Exception as e:
        print(f"[log:ERROR] 獲取 {stockNumber} 的股票名稱失敗: {e}")
        return "no"

def draw_kchart(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no":
        return "股票代碼錯誤!"
    
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=365)
    stock = yf.Ticker(stockNumber + '.TW')
    df = stock.history(start=start, end=end)
    if df.empty:
        print(f"[log:ERROR] 無法獲取 {stockNumber}.TW 的數據")
        return "無法獲取股票數據!"
    
    print(f"[log:DEBUG] 數據形狀: {df.shape}")
    print(f"[log:DEBUG] 數據樣本: \n{df.tail(5)}")

    print("[log:INFO] 開始生成圖表")
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=f'{stock_name} K線圖',
        ylabel='價格',
        volume=True,
        mav=(5, 10, 20, 60),
        savefig='kchart.png'
    )
    
    if not os.path.exists('kchart.png') or os.path.getsize('kchart.png') == 0:
        print(f"[log:ERROR] kchart.png 為空或未創建!")
        return "圖表生成失敗，請稍後再試!"
    
    print(f"[log:INFO] 圖表已保存至 kchart.png")
    img_url = Imgur.showImgur("kchart")  # 修正檔案名稱一致性
    if not img_url.startswith("https"):
        print(f"[log:ERROR] Imgur 上傳失敗: {img_url}")
        return "圖片上傳失敗，請稍後再試!"
    print(f"[log:INFO] 圖表已上傳: {img_url}")
    return img_url
