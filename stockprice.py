''' 
即時股價與走勢圖
'''
import requests  # HTTP請求庫，用於從網路上抓取資料
import datetime  # 日期時間處理庫，用於日期計算
import pandas as pd  # 資料處理庫，用於表格數據操作
import yfinance as yf  # Yahoo Finance API，用於獲取股票歷史數據
from bs4 import BeautifulSoup  # HTML解析庫，用於提取網頁內容
import Imgur  # 自定義模組（假設用於將圖片上傳至Imgur）
import matplotlib  # 繪圖基礎庫
import matplotlib.pyplot as plt  # Matplotlib的子模組，用於繪圖
from matplotlib.font_manager import FontProperties  # 字體管理模組，用於設定中文字體

# 設定中文字體
chinese_font = matplotlib.font_manager.FontProperties(fname='msjh.ttf')  # 引入同個資料夾下的微軟正黑體字體檔案

# Emoji 定義，用於美化輸出訊息
emoji_upinfo = u'\U0001F447'  # 向下箭頭
emoji_midinfo = u'\U0001F538'  # 小橘色圓點
emoji_downinfo = u'\U0001F60A'  # 笑臉

# 從Yahoo Finance獲取股票名稱
def get_stock_name(stockNumber):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockNumber}.TW'  # 構造Yahoo Finance台灣股票頁面URL
        # 設定User-Agent模擬瀏覽器，避免被阻擋
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        page = requests.get(url, headers=headers)  # 發送HTTP GET請求
        soup = BeautifulSoup(page.content, 'html.parser')  # 使用BeautifulSoup解析HTML內容
        # 尋找股票名稱的標籤（h1標籤，特定class）
        stock_name = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)').text
        return stock_name  # 回傳股票名稱
    except Exception as e:
        print(f"[log:ERROR] Error in get_stock_name: {e}")  # 記錄錯誤訊息
        return "no"  # 回傳"no"表示失敗

# 使用者查詢股票即時資訊
def getprice(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)  # 獲取股票名稱
    if stock_name == "no":
        return "股票代碼錯誤!"  # 若名稱獲取失敗，回傳錯誤訊息
    content = ""
    stock = yf.Ticker(stockNumber + '.TW')  # 使用yfinance創建台灣股票對象（.TW為台股後綴）
    hist = stock.history(period="5d")  # 獲取近5天的歷史數據
    if hist.empty:
        return "無法獲取股票數據，請確認代碼或稍後再試!"  # 若數據為空，回傳錯誤訊息
    
    date = hist.index[-1].strftime('%Y-%m-%d')  # 最新交易日期
    price = '%.2f' % hist["Close"].iloc[-1]  # 最新收盤價，保留兩位小數
    last_price = '%.2f' % hist["Close"].iloc[-2]  # 前一日收盤價
    spread_price = '%.2f' % (float(price) - float(last_price))  # 計算價差
    spread_ratio = '%.2f' % (float(spread_price) / float(last_price) * 100) + '%'  # 計算漲跌幅百分比
    # 根據漲跌情況添加符號（△為漲，▽為跌）
    spread_price = spread_price.replace("-", "▽ ") if float(last_price) > float(price) else "△ " + spread_price
    spread_ratio = spread_ratio.replace("-", "▽ ") if float(last_price) > float(price) else "△ " + spread_ratio
    open_price = '%.2f' % hist["Open"].iloc[-1]  # 開盤價
    high_price = '%.2f' % hist["High"].iloc[-1]  # 最高價
    low_price = '%.2f' % hist["Low"].iloc[-1]  # 最低價
    price_five = hist["Close"].iloc[-5:]  # 近五日收盤價
    stockAverage = '%.2f' % price_five.mean()  # 近五日平均價格
    stockSTD = '%.2f' % price_five.std()  # 近五日標準差
    
    # 組合股票資訊訊息，包含Emoji美化
    content += f"{stock_name} 股票報告{emoji_upinfo}\n--------------\n日期: {date}\n{emoji_midinfo}最新收盤價: {price}\n{emoji_midinfo}開盤價: {open_price}\n{emoji_midinfo}最高價: {high_price}\n{emoji_midinfo}最低價: {low_price}\n{emoji_midinfo}漲跌價差: {spread_price} 漲跌幅: {spread_ratio}\n{emoji_midinfo}五日平均價格: {stockAverage}\n{emoji_midinfo}五日標準差: {stockSTD}\n"
    if msg.startswith("#"):
        content += f"--------------\n請選擇下方選項查看更多詳情{emoji_downinfo}"  # 若輸入以#開頭，提示更多選項
    else:
        content += '\n'
    return content

# 繪製近一年股價走勢圖
def stock_trend(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)  # 獲取股票名稱
    if stock_name == "no":
        return "股票代碼錯誤!"  # 若名稱獲取失敗，回傳錯誤訊息

    end = datetime.datetime.now()  # 設定結束日期為當前時間
    date = end.strftime("%Y%m%d")  # 格式化當前日期
    year = str(int(date[0:4]) - 1)  # 計算一年前的年份
    month = date[4:6]  # 當前月份
    
    stock = yf.Ticker(stockNumber + '.TW')  # 創建台灣股票對象
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)  # 獲取近一年歷史數據
    
    if stock_data.empty:
        print(f"[log:ERROR] No trend data for {stockNumber}.TW")  # 若數據為空，記錄錯誤
        return "no"  # 回傳"no"表示失敗
    
    plt.figure(figsize=(12, 6))  # 設定圖表尺寸
    plt.plot(stock_data["Close"], '-', label="收盤價")  # 繪製收盤價折線
    plt.plot(stock_data["High"], '-', label="最高價")  # 繪製最高價折線
    plt.plot(stock_data["Low"], '-', label="最低價")  # 繪製最低價折線
    plt.title(f'{stock_name} 近一年價格走勢', loc='center', fontsize=20, fontproperties=chinese_font)  # 設定標題
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)  # X軸標籤
    plt.ylabel('價格', fontsize=20, fontproperties=chinese_font)  # Y軸標籤
    plt.grid(True, axis='y')  # 顯示Y軸網格線
    plt.legend(fontsize=14, prop=chinese_font)  # 顯示圖例並使用中文字體
    plt.savefig(msg + '.png')  # 儲存圖表，檔案名稱為輸入的msg
    plt.close()  # 關閉繪圖窗口
    
    return Imgur.showImgur(msg)  # 上傳圖片至Imgur並回傳URL

# 繪製近一年股票收益率走勢圖
def show_return(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)  # 獲取股票名稱
    if stock_name == "no":
        return "股票代碼錯誤!"  # 若名稱獲取失敗，回傳錯誤訊息

    end = datetime.datetime.now()  # 設定結束日期為當前時間
    date = end.strftime("%Y%m%d")  # 格式化當前日期
    year = str(int(date[0:4]) - 1)  # 計算一年前的年份
    month = date[4:6]  # 當前月份
    
    stock = yf.Ticker(stockNumber + '.TW')  # 創建台灣股票對象
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)  # 獲取近一年歷史數據
    
    if stock_data.empty:
        print(f"[log:ERROR] No return data for {stockNumber}.TW")  # 若數據為空，記錄錯誤
        return "no"  # 回傳"no"表示失敗
    
    stock_data['Returns'] = stock_data['Close'].pct_change()  # 計算每日收益率（百分比變化）
    stock_return = stock_data['Returns'].dropna()  # 移除無效數據
    
    plt.figure(figsize=(12, 6))  # 設定圖表尺寸
    plt.plot(stock_return, label="收益率")  # 繪製收益率折線
    plt.title(f'{stock_name} 近一年收益率走勢', loc='center', fontsize=20, fontproperties=chinese_font)  # 設定標題
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)  # X軸標籤
    plt.ylabel('收益率', fontsize=20, fontproperties=chinese_font)  # Y軸標籤
    plt.grid(True, axis='y')  # 顯示Y軸網格線
    plt.legend(fontsize=14, prop=chinese_font)  # 顯示圖例並使用中文字體
    plt.savefig(msg + '.png')  # 儲存圖表，檔案名稱為輸入的msg
    plt.close()  # 關閉繪圖窗口
    
    return Imgur.showImgur(msg)  # 上傳圖片至Imgur並回傳URL

# 繪製近一年股價震盪圖
def show_fluctuation(stockNumber, msg):
    stock_name = get_stock_name(stockNumber)  # 獲取股票名稱
    if stock_name == "no":
        return "股票代碼錯誤!"  # 若名稱獲取失敗，回傳錯誤訊息

    end = datetime.datetime.now()  # 設定結束日期為當前時間
    date = end.strftime("%Y%m%d")  # 格式化當前日期
    year = str(int(date[0:4]) - 1)  # 計算一年前的年份
    month = date[4:6]  # 當前月份
    
    stock = yf.Ticker(stockNumber + '.TW')  # 創建台灣股票對象
    stock_data = stock.history(start=f"{year}-{month}-01", end=end)  # 獲取近一年歷史數據
    
    if stock_data.empty:
        print(f"[log:ERROR] No fluctuation data for {stockNumber}.TW")  # 若數據為空，記錄錯誤
        return "no"  # 回傳"no"表示失敗
    
    stock_data['stock_fluctuation'] = stock_data["High"] - stock_data["Low"]  # 計算每日震盪幅度（最高價-最低價）
    
    plt.figure(figsize=(12, 6))  # 設定圖表尺寸
    plt.plot(stock_data['stock_fluctuation'], '-', label="震盪幅度", color="orange")  # 繪製震盪幅度折線，橙色
    plt.title(f'{stock_name} 近一年價格震盪', loc='center', fontsize=20, fontproperties=chinese_font)  # 設定標題
    plt.xlabel('日期', fontsize=20, fontproperties=chinese_font)  # X軸標籤
    plt.ylabel('價格', fontsize=20, fontproperties=chinese_font)  # Y軸標籤
    plt.grid(True, axis='y')  # 顯示Y軸網格線
    plt.legend(fontsize=14, prop=chinese_font)  # 顯示圖例並使用中文字體
    plt.savefig(msg + '.png')  # 儲存圖表，檔案名稱為輸入的msg
    plt.close()  # 關閉繪圖窗口
    
    return Imgur.showImgur(msg)  # 上傳圖片至Imgur並回傳URL
