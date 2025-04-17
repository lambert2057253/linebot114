import twder  # 台灣匯率資料庫，用於獲取台幣與外幣的匯率
import pandas as pd  # 資料處理庫，用於表格數據操作
import requests  # HTTP請求庫，用於從網路上獲取資料
import json  # JSON處理庫，用於解析API回傳的JSON數據
import matplotlib.pyplot as plt  # 繪圖庫，用於生成匯率走勢圖
import Imgur  # 自定義模組（假設用於將圖片上傳至Imgur）
import numpy as np  # 數值運算庫，用於數學計算
import matplotlib  # Matplotlib基礎庫，用於繪圖設定
import ssl  # SSL模組，用於處理HTTPS請求的安全性
ssl._create_default_https_context = ssl._create_unverified_context  # 忽略未驗證的HTTPS證書
from matplotlib.font_manager import FontProperties  # 字體管理模組，用於設定中文字體
chinese_font = matplotlib.font_manager.FontProperties(fname='msjh.ttf')  # 引入支援繁體中文的字體檔案（假設為微軟正黑體）

# 定義貨幣名稱字典，將貨幣代碼轉換為中文名稱
def getCurrencyName(currency):
    currency_list = { 
        "USD" : "美元",
        "JPY": "日圓",
        "HKD" :"港幣",
        "GBP" : "英鎊",
        "AUD" : "澳幣",
        "CAD" : "加拿大幣",
        "CHF" : "瑞士法郎",  
        "SGD" : "新加坡幣",
        "ZAR" : "南非幣",
        "SEK" : "瑞典幣",
        "NZD" : "紐元", 
        "THB" : "泰幣", 
        "PHP" : "菲國比索", 
        "IDR" : "印尼幣", 
        "KRW" : "韓元",   
        "MYR" : "馬來幣", 
        "VND" : "越南盾", 
        "CNY" : "人民幣",
    }
    try: 
        currency_name = currency_list[currency]  # 嘗試根據代碼獲取中文名稱
    except: 
        return "無可支援的外幣"  # 若代碼不在字典中，回傳錯誤訊息
    return currency_name

# 外幣兌換功能，將指定金額的外幣兌換為台幣
def exchange_currency(code) :
    condition = code[0:2]  # 前兩個字元表示"買入"或"賣出"
    code = code.strip(code[0:4])  # 移除前4個字元（如"買入"或"賣出"加上分隔符）
    currency = code[0:3]  # 提取貨幣代碼（如USD）
    currency_name = getCurrencyName(currency)  # 獲取貨幣中文名稱
    if currency_name == "無可支援的外幣": 
        return "無可支援的外幣"  # 若貨幣不受支援，回傳錯誤訊息
    amount = float(code[3:])  # 提取金額並轉為浮點數
    currency = twder.now(currency)  # 使用twder獲取該貨幣的即時匯率資料
    now_time = str(currency[0])  # 獲取最新掛牌時間
    content = currency_name + "最新掛牌時間為: " + now_time  # 建立回傳訊息
    if condition == "賣出":  # 若使用者想賣外幣給銀行（即銀行買入）
        buying_spot = "無資料" if currency[3] == '-' else float(currency[3])  # 銀行即期買入價格
        if buying_spot == "無資料": 
            return "此外幣無即期買入匯率"  # 若無資料，回傳錯誤訊息
        outcome = str('%.2f ' % (amount * buying_spot))  # 計算兌換結果並保留兩位小數
        content += '\n即期買入價格: ' + str(buying_spot)  # 加入即期買入價格資訊
    else:  # 若使用者想買外幣（即銀行賣出）
        sold_spot = "無資料" if currency[4] == '-' else float(currency[4])  # 銀行即期賣出價格
        if sold_spot == "無資料": 
            return "此外幣無即期賣出匯率"  # 若無資料，回傳錯誤訊息
        outcome = str('%.2f ' % (amount * sold_spot))  # 計算兌換結果並保留兩位小數
        content += f'\n即期賣出價格: {sold_spot}'  # 加入即期賣出價格資訊

    content += f"\n換匯結果為台幣 {outcome}元"  # 加入最終兌換結果
    return content

# 查詢指定貨幣的即時匯率資訊
def showCurrency(code) -> "JPY":  # 輸入貨幣代碼，回傳匯率資訊
    content = ""
    currency_name = getCurrencyName(code)  # 獲取貨幣中文名稱
    if currency_name == "無可支援的外幣": 
        return "無可支援的外幣"  # 若貨幣不受支援，回傳錯誤訊息
    currency = twder.now(code)  # 使用twder獲取該貨幣的即時匯率資料
    now_time = str(currency[0])  # 最新掛牌時間
    buying_cash = "無資料" if currency[1] == '-' else str(float(currency[1]))  # 現金買入價格
    sold_cash = "無資料" if currency[2] == '-' else str(float(currency[2]))  # 現金賣出價格
    buying_spot = "無資料" if currency[3] == '-' else str(float(currency[3]))  # 即期買入價格
    sold_spot = "無資料" if currency[4] == '-' else str(float(currency[4]))  # 即期賣出價格

    # 組合回傳訊息，包含所有匯率資訊
    content += f"{currency_name} 最新掛牌時間為: {now_time}\n ---------- \n 現金買入價格: {buying_cash}\n 現金賣出價格: {sold_cash}\n 即期買入價格: {buying_spot}\n 即期賣出價格: {sold_spot}\n \n"
    return content

# 繪製過去六個月的即期匯率走勢圖
def spot_exrate_sixMonth(code2):
    currency_name = getCurrencyName(code2)  # 獲取貨幣中文名稱
    if currency_name == "無可支援的外幣": 
        return "無可支援的外幣"  # 若貨幣不受支援，回傳錯誤訊息
    dfs = pd.read_html(f'https://rate.bot.com.tw/xrt/quote/l6m/{code2}')  # 從台灣銀行網站抓取六個月資料
    currency = dfs[0].iloc[:, 0:6]  # 提取前6欄數據
    currency.columns = [u'Date', u'Currency', u'現金買入', u'現金賣出', u'即期買入', u'即期賣出']  # 設定欄位名稱
    currency[u'Currency'] = currency[u'Currency'].str.extract('\((\w+)\)')  # 提取貨幣代碼
    currency = currency.iloc[::-1]  # 反轉資料順序（從舊到新）
    if currency["即期買入"][0] == "-" or currency["即期買入"][0] == 0.0:
        return "即期匯率無資料可分析"  # 若無即期匯率資料，回傳錯誤訊息
    currency.plot(kind='line', figsize=(12, 6), x='Date', y=[u'即期買入', u'即期賣出'])  # 繪製折線圖
    plt.legend(prop=chinese_font)  # 設定圖例為中文字體
    plt.title(f"{currency_name} 即期匯率", fontsize=20, fontproperties=chinese_font)  # 設定標題
    plt.savefig(f"{code2}.png")  # 儲存圖片
    plt.show()  # 顯示圖片
    plt.close()  # 關閉繪圖窗口
    return Imgur.showImgur(code2)  # 上傳圖片至Imgur並回傳連結

# 繪製過去六個月的現金匯率走勢圖
def cash_exrate_sixMonth(code1):
    currency_name = getCurrencyName(code1)  # 獲取貨幣中文名稱
    if currency_name == "無可支援的外幣": 
        return "無可支援的外幣"  # 若貨幣不受支援，回傳錯誤訊息
    dfs = pd.read_html(f'https://rate.bot.com.tw/xrt/quote/l6m/{code1}')  # 從台灣銀行網站抓取六個月資料
    currency = dfs[0].iloc[:, 0:6]  # 提取前6欄數據
    currency.columns = [u'Date', u'Currency', u'現金買入', u'現金賣出', u'即期買入', u'即期賣出']  # 設定欄位名稱
    currency[u'Currency'] = currency[u'Currency'].str.extract('\((\w+)\)')  # 提取貨幣代碼
    currency = currency.iloc[::-1]  # 反轉資料順序（從舊到新）
    if currency["現金買入"][0] == "-" or currency["現金買入"][0] == 0.0:
        return "現金匯率無資料可分析"  # 若無現金匯率資料，回傳錯誤訊息
    currency.plot(kind='line', figsize=(12, 6), x='Date', y=[u'現金買入', u'現金賣出'])  # 繪製折線圖
    plt.legend(prop=chinese_font)  # 設定圖例為中文字體
    plt.title(currency_name + " 現金匯率", fontsize=20, fontproperties=chinese_font)  # 設定標題
    plt.savefig(f"{code1}.png")  # 儲存圖片
    plt.show()  # 顯示圖片
    plt.close()  # 關閉繪圖窗口
    return Imgur.showImgur(code1)  # 上傳圖片至Imgur並回傳連結

# 獲取所有支援貨幣的即期賣出匯率列表
def get_currency_list():
    currency_list = twder.now_all()  # 獲取所有貨幣的即時匯率資料
    currency_list = list(currency_list.values())  # 轉為列表
    currencies = []
    for i in range(len(currency_list)):
        currencies.append(currency_list[i][4])  # 提取即期賣出價格
    return currencies

# 使用Coinbase API查詢不同貨幣間的即時兌換率（不限於台幣）
def getExchangeRate(msg): 
    """
    範例輸入：
    code = '換匯USD/TWD/100'  # 將100美元兌換為台幣
    code = '換匯USD/JPY/100'  # 將100美元兌換為日圓
    """
    currency_list = msg[2:].split("/")  # 解析輸入訊息，移除"換匯"前綴並以"/"分割
    currency = currency_list[0]  # 第一個貨幣代碼（兌換來源）
    currency1 = currency_list[1]  # 第二個貨幣代碼（兌換目標）
    money_value = currency_list[2]  # 兌換金額
    url_coinbase = 'https://api.coinbase.com/v2/exchange-rates?currency=' + currency  # Coinbase API端點
    res = requests.get(url_coinbase)  # 發送GET請求
    jData = res.json()  # 解析JSON回應
    pd_currency = jData['data']['rates']  # 提取匯率資料
    content = f'目前的兌換率為:{pd_currency[currency1]} {currency1} \n查詢的金額為: '  # 組合回傳訊息
    amount = float(pd_currency[currency1])  # 將匯率轉為浮點數
    content += str('%.2f' % (amount * float(money_value))) + " " + currency1  # 計算並加入兌換結果
    return content
