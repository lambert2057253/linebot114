# kchart.py
import pandas as pd  # 資料處理庫，用於處理表格數據
import yfinance as yf  # Yahoo Finance API，用於獲取股票歷史數據
import mplfinance as mpf  # 繪製K線圖的庫
import requests  # HTTP請求庫，用於從網路上抓取資料
from bs4 import BeautifulSoup  # HTML解析庫，用於提取網頁內容
import datetime  # 日期時間處理庫
import Imgur  # 自定義模組（假設用於將圖片上傳至Imgur）
import os  # 作業系統接口，用於檔案操作
import matplotlib  # 繪圖基礎庫
import matplotlib.pyplot as plt  # Matplotlib的子模組，用於繪圖
from matplotlib.font_manager import FontProperties  # 字體管理模組，用於設定中文字體

# 設定全局中文字體，避免中文顯示問題
font_path = '/opt/render/project/src/msjh.ttf'  # 指定微軟正黑體字體檔案的絕對路徑（適用於Render環境）
matplotlib.rcParams['font.family'] = 'sans-serif'  # 設定字體家族為sans-serif
matplotlib.rcParams['font.sans-serif'] = [font_path]  # 直接使用字體檔案路徑
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號無法正常顯示的問題

# 從Yahoo Finance獲取股票名稱
def get_stock_name(stockNumber):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockNumber}.TW'  # 構造Yahoo Finance台灣股票頁面URL
        # 設定User-Agent模擬瀏覽器，避免被阻擋
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        page = requests.get(url, headers=headers)  # 發送HTTP GET請求
        page.raise_for_status()  # 若請求失敗，拋出異常
        soup = BeautifulSoup(page.content, 'html.parser')  # 使用BeautifulSoup解析HTML內容
        # 尋找股票名稱的標籤（h1標籤，特定class）
        stock_name = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)')
        if stock_name:
            return stock_name.text.strip()  # 移除多餘空白並回傳股票名稱
        print(f"[log:WARNING] 找不到 {stockNumber} 的股票名稱")  # 若未找到名稱，記錄警告
        return "no"  # 回傳"no"表示失敗
    except Exception as e:
        print(f"[log:ERROR] 獲取 {stockNumber} 的股票名稱失敗: {e}")  # 記錄錯誤訊息
        return "no"  # 回傳"no"表示失敗

# 繪製並上傳股票K線圖
def draw_kchart(stockNumber):
    stock_name = get_stock_name(stockNumber)  # 獲取股票名稱
    if stock_name == "no":
        return "股票代碼錯誤!"  # 若名稱獲取失敗，回傳錯誤訊息
    
    end = datetime.datetime.now()  # 設定結束日期為當前時間
    start = end - datetime.timedelta(days=365)  # 設定開始日期為過去365天
    stock = yf.Ticker(stockNumber + '.TW')  # 使用yfinance創建台灣股票對象（.TW為台股後綴）
    df = stock.history(start=start, end=end)  # 獲取指定日期範圍的歷史數據
    if df.empty:
        print(f"[log:ERROR] 無法獲取 {stockNumber}.TW 的數據")  # 若數據為空，記錄錯誤
        return "無法獲取股票數據!"  # 回傳錯誤訊息
    
    # 記錄數據資訊以便除錯
    print(f"[log:DEBUG] 數據形狀: {df.shape}")  # 顯示數據的行數和列數
    print(f"[log:DEBUG] 數據樣本: \n{df.tail(5)}")  # 顯示最後五筆數據樣本

    print("[log:INFO] 開始生成圖表")  # 記錄圖表生成開始
    # 使用mplfinance繪製K線圖
    mpf.plot(
        df,  # 股票歷史數據
        type='candle',  # 圖表類型為K線圖
        style='charles',  # 使用charles風格（預定義的配色）
        title=f'{stock_name} K線圖',  # 圖表標題，包含股票名稱
        ylabel='價格',  # Y軸標籤
        volume=True,  # 顯示成交量
        mav=(5, 10, 20, 60),  # 加入5、10、20、60日均線
        savefig='kchart.png'  # 將圖表儲存為kchart.png
    )
    
    # 檢查圖表檔案是否成功生成
    if not os.path.exists('kchart.png') or os.path.getsize('kchart.png') == 0:
        print(f"[log:ERROR] kchart.png 為空或未創建!")  # 若檔案不存在或為空，記錄錯誤
        return "圖表生成失敗，請稍後再試!"  # 回傳錯誤訊息
    
    print(f"[log:INFO] 圖表已保存至 kchart.png")  # 記錄圖表儲存成功
    img_url = Imgur.showImgur("kchart")  # 將圖表上傳至Imgur並獲取URL（假設功能）
    if not img_url.startswith("https"):
        print(f"[log:ERROR] Imgur 上傳失敗: {img_url}")  # 若上傳失敗，記錄錯誤
        return "圖片上傳失敗，請稍後再試!"  # 回傳錯誤訊息
    print(f"[log:INFO] 圖表已上傳: {img_url}")  # 記錄上傳成功並顯示URL
    return img_url  # 回傳圖片URL
