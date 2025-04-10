'''
Created by Tsung Yu on 17/03/2020.
Copyright © 2020 Tsung Yu. All rights reserved.
'''
# 系統與第三方模組
import re  # 正規表示式，用來比對使用者輸入指令
from pymongo import MongoClient  # 用來連接 MongoDB 資料庫
import pymongo  # 匯入完整的 pymongo 套件（保留使用彈性）
import os  # 作業系統相關操作，例如讀取環境變數
import urllib.parse  # URL 轉換處理

# 專案內自訂模組
import EXRate  # 外匯相關功能模組
import kchart  # 股票 K 線圖模組
import news  # 新聞模組
import stockprice  # 股價查詢模組
import Institutional_Investors  # 三大法人資料模組
import stock_compare  # 股票比較模組
import Technical_Analysis  # 技術分析模組
import Technical_Analysis_test  # 技術分析模擬測試模組

# LINE BOT 回覆訊息的樣板模組
from msg_template import Msg_fundamental_ability  # 股票基本面能力分析訊息
from msg_template import Msg_Template  # 一般訊息樣板
from msg_template import questionnaire  # 問卷系統訊息
from msg_template import Msg_Exrate  # 外匯訊息樣板
from msg_template import Msg_News  # 新聞訊息樣板
from msg_template import Msg_diagnose  # 股票健診訊息樣板

# 其他分析模組
import new_famous_book  # 新書榜資料
import Fundamental_Analysis  # 基本面分析模組
# Flask Web 框架
from flask import Flask, request, abort

# LINE BOT SDK
from linebot import (
    LineBotApi, WebhookHandler  # 用來處理 LINE 的 API 與 webhook 請求
)
from linebot.exceptions import (
    InvalidSignatureError  # 用來處理簽章驗證失敗的例外
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage  # 處理訊息事件與回覆格式
)

# 建立 Flask 應用實體
app = Flask(__name__)

# 初始化 LINE Bot API 與 WebhookHandler（需使用自己的 token 與 secret）
line_bot_api = LineBotApi('你的 channel access token')
handler = WebhookHandler('你的 channel secret')

# 預設通知對象（自己的 user id）
my_user_id = 'U85ee49b7fb6269266e497110c4ac6e9c'

# 啟動 bot 時，主動推送一條文字訊息給指定用戶
line_bot_api.push_message(my_user_id, TextSendMessage(text="start"))
@app.route("/")
def home():
    return "home"  # 根目錄路由，回傳字串 "home"
# MongoDB 資料庫連線設定（從環境變數讀取，若無則使用預設連線字串）
mongo_uri = os.getenv(
    'MONGODB_URI',
    'mongodb+srv://davidpatty11:phyozdas369@cluster0.aynxh0o.mongodb.net/stock_db?retryWrites=true&w=majority'
)

# 連接 MongoDB
client = MongoClient(mongo_uri)

# 指定資料庫與集合（collection）
db = client['stock_db']
collection = db['prices']
@app.route("/callback", methods=['POST'])
def callback():
    # 從 header 取得 LINE 傳來的簽章（用來驗證安全性）
    signature = request.headers['X-Line-Signature']

    # 取得 POST 的資料本體（純文字）
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)  # 將收到的訊息寫入 log

    try:
        handler.handle(body, signature)  # 嘗試處理事件
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)  # 驗證失敗則拒絕請求

    return 'OK'  # 成功處理回傳 OK
# 註冊訊息事件處理器，當收到文字訊息時觸發此函式
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得使用者輸入訊息，轉大寫並移除多餘空白
    msg = str(event.message.text).upper().strip()

    # 取得使用者 LINE 資訊
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name  # 顯示名稱
    uid = profile.user_id  # 使用者 LINE 的 ID
# 如果使用者輸入「問卷分析」
if re.match("問卷分析", msg):
    # 發送歡迎訊息與第一題
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.greeting_msg))
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q1))

    # 顯示第一題的選項（Flex message）
    content = questionnaire.Q1_menu()
    line_bot_api.push_message(uid, content)
    return 0  # 中止處理
# 顯示第二題
elif re.match("Q2", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q2))
    line_bot_api.push_message(uid, questionnaire.Q2_menu())
    return 0

# 顯示第三題
elif re.match("Q3", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q3))
    line_bot_api.push_message(uid, questionnaire.Q3_menu())
    return 0

# 顯示第四題
elif re.match("Q4", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q4))
    line_bot_api.push_message(uid, questionnaire.Q4_menu())
    return 0

# 顯示第五題
elif re.match("Q5", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q5))
    line_bot_api.push_message(uid, questionnaire.Q5_menu())
    return 0

# 顯示第六題
elif re.match("Q6", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q6))
    line_bot_api.push_message(uid, questionnaire.Q6_menu())
    return 0

# 顯示第七題
elif re.match("Q7", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q7))
    line_bot_api.push_message(uid, questionnaire.Q7_menu())
    return 0

# 顯示第八題
elif re.match("Q8", msg):
    line_bot_api.push_message(uid, TextSendMessage(questionnaire.Q8))
    line_bot_api.push_message(uid, questionnaire.Q8_menu())
    return 0
# 使用者輸入「類型A」時，推播對應圖片
elif re.match("類型A", msg):
    img_url = questionnaire.type_A
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0

# 使用者輸入「類型B」
elif re.match("類型B", msg):
    img_url = questionnaire.type_B
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0

# 使用者輸入「類型C」～「類型J」
elif re.match("類型C", msg):
    img_url = questionnaire.type_C
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型D", msg):
    img_url = questionnaire.type_D
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型E", msg):
    img_url = questionnaire.type_E
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型F", msg):
    img_url = questionnaire.type_F
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型G", msg):
    img_url = questionnaire.type_G
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型H", msg):
    img_url = questionnaire.type_H
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型I", msg):
    img_url = questionnaire.type_I
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
elif re.match("類型J", msg):
    img_url = questionnaire.type_J
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0
# 使用者輸入「新書榜」
elif re.match("新書榜", msg):
    line_bot_api.push_message(uid, TextSendMessage("將給您最新理財新書......"))
    flex_message = Msg_Template.new_books()  # 呼叫模板取得 Flex Message
    line_bot_api.push_message(uid, flex_message)
    return 0

# 使用者輸入「暢銷榜」
elif re.match("暢銷榜", msg):
    line_bot_api.push_message(uid, TextSendMessage("將給您最新理財暢銷書......"))
    flex_message = Msg_Template.famous_books()  # 呼叫模板取得 Flex Message
    line_bot_api.push_message(uid, flex_message)
    return 0
# 使用者輸入 /股票，顯示股票與 ETF 選單
elif re.match("/股票", msg):
    content = Msg_Template.menu_stock_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    content = Msg_Template.menu_etf_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 使用者輸入 /理財，顯示理財選單
elif re.match("/理財", msg):
    content = Msg_Template.menu_fin_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 使用者輸入 外匯列表，顯示即時匯率查詢選單
elif re.match("外匯列表", msg):
    content = Msg_Exrate.realtime_menu()
    line_bot_api.push_message(uid, content)
    return 0

# 使用者輸入 /外匯，顯示外匯功能選單
elif re.match("/外匯", msg):
    content = Msg_Template.menu_exrate_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 使用者輸入 /我的收藏，顯示收藏清單選單
elif re.match("/我的收藏", msg):
    content = Msg_Template.menu_mylist_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 使用者輸入 #股票健診，顯示健診功能主選單
elif re.match("#股票健診", msg):
    content = Msg_diagnose.diagnose_menu()
    line_bot_api.push_message(uid, content)
    return 0

# 使用者輸入 /產業文章，顯示產業相關文章選單
elif re.match("/產業文章", msg):
    content = Msg_Template.industrial_artical()
    line_bot_api.push_message(uid, content)
    return 0

# 使用者輸入 理財YOUTUBER推薦，顯示推薦頻道
elif re.match("理財YOUTUBER推薦", msg):
    content = Msg_Template.youtube_channel()
    line_bot_api.push_message(uid, content)
    return 0
# 使用者輸入「關注+股票代號」，例如「關注2330」
elif re.match('關注[0-9]{4}', msg):
    stockNumber = msg[2:6]  # 擷取股票代號
    stockName = stockprice.get_stock_name(stockNumber)  # 取得股票名稱

    if stockName == "no":
        content = "股票代碼錯誤"
    else:
        line_bot_api.push_message(uid, TextSendMessage("加入股票代號" + stockNumber))

        # 若有設定股價提醒條件（例如：關注2330>500）
        if re.match('關注[0-9]{4}[<>][0-9]', msg):
            content = mongodb.write_my_stock(uid, user_name, stockNumber, msg[6:7], msg[7:])
        else:
            content = mongodb.write_my_stock(uid, user_name, stockNumber, "未設定", "未設定")

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 股票教學選單
elif re.match("股票教學", msg):
    content = Msg_Template.stock_info_menu()
    line_bot_api.push_message(uid, content)
    return 0

# 外匯教學訊息
elif re.match("外匯教學", msg):
    content = Msg_Exrate.Exrate_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 快樂學理財選單
elif re.match("快樂學理財", msg):
    content = Msg_Template.learning_menu()
    line_bot_api.push_message(uid, content)
    return 0
# 三大投資分析總表圖片
elif re.match("三大投資分析表", msg):
    img_url = "https://i.imgur.com/StGNRGR.png"
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    return 0

# 單獨查詢「基本面」說明
elif re.match("基本面", msg):
    content = Msg_Template.three_investment(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 技術面說明
elif re.match("技術面", msg):
    content = Msg_Template.three_investment(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 籌碼面說明
elif re.match("籌碼面", msg):
    content = Msg_Template.three_investment(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 保守型投資者說明
elif re.match("保守型投資者", msg):
    content = Msg_Template.investor_type(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 激進型投資者說明
elif re.match("激進型投資者", msg):
    content = Msg_Template.investor_type(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 獨立型投資者說明
elif re.match("獨立型投資者", msg):
    content = Msg_Template.investor_type(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# EPS 說明
elif re.match("EPS", msg):
    content = Msg_Template.proper_noun(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 買超/賣超 說明
elif re.match("買超/賣超", msg):
    content = Msg_Template.proper_noun(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 多頭市場/空頭市場 說明
elif re.match("多頭市場/空頭市場", msg):
    content = Msg_Template.proper_noun(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 黃金交叉/死亡交叉 說明
elif re.match("黃金交叉/死亡交叉", msg):
    content = Msg_Template.proper_noun(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 推薦理財電影清單
elif re.match("理財電影", msg):
    content = Msg_Template.movies()
    line_bot_api.push_message(uid, content)
    return 0

# 推薦理財書籍清單
elif re.match("理財書籍", msg):
    content = Msg_Template.fin_books()
    line_bot_api.push_message(uid, content)
    return 0
# 使用者輸入「比較+股票代碼」，範例：比較2330/2002/2317
elif re.match("比較", msg):
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 我們將會給您這幾檔股票收盤價走勢圖...'))

    img_url = stock_compare.show_pic(msg)  # 呼叫模組產生走勢圖

    if img_url == "no":
        line_bot_api.push_message(uid, TextSendMessage('股票代碼錯誤'))
    else:
        line_bot_api.push_message(uid, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
# 使用者輸入「#股票代碼」，查詢單一股票
elif re.match('#[0-9]', msg):
    stockNumber = msg[1:]  # 取得股票代號
    stockName = stockprice.get_stock_name(stockNumber)

    if stockName == "no":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤"))
    else:
        line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 查詢編號: {stockNumber} 的股價中...'))
        content_text = stockprice.getprice(stockNumber, msg)
        content = Msg_Template.stock_reply(stockNumber, content_text)
        line_bot_api.push_message(uid, content)
    return 0
# 使用者輸入「三大面向分析2330」
elif re.match("三大面向分析[0-9]", msg):
    stockNumber = msg.strip("三大面向分析")  # 擷取代號
    content = Msg_Template.stock_ananlysis_menu(stockNumber)
    line_bot_api.push_message(uid, content)
    return 0
# 技術面分析（股票技術面2330）
elif re.match('股票技術面[0-9]', msg):
    stockNumber = msg.strip("股票技術面")
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 分析編號: {stockNumber}的股價中...'))
    content = Msg_Template.stock_tec_analysis(stockNumber)
    line_bot_api.push_message(uid, content)
    return 0

# 基本面分析（股票基本面2330）
elif re.match('股票基本面[0-9]{4}', msg):
    stockNumber = msg.strip("股票基本面")
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 分析編號: {stockNumber}基本面中...'))
    content = Msg_Template.stock_fundation_analysis(stockNumber)
    line_bot_api.push_message(uid, content)
    return 0
# 經營能力分析：使用者輸入「經營能力2330」
elif re.match("經營能力[0-9]{4}", msg):
    stockNumber = msg.strip("經營能力")
    stockName = stockprice.get_stock_name(stockNumber)
    line_bot_api.push_message(uid, TextSendMessage(f"正在為您分析股票代號: {stockNumber} 的經營能力......"))

    if stockName == "no":
        content = "股票代碼錯誤"
    else:
        content = Msg_fundamental_ability.operating_ability(stockNumber, stockName)

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 償債能力分析：輸入「償債能力2330」
elif re.match("償債能力[0-9]{4}", msg):
    stockNumber = msg.strip("償債能力")
    stockName = stockprice.get_stock_name(stockNumber)
    line_bot_api.push_message(uid, TextSendMessage(f"正在為您分析股票代號: {stockNumber} 的償債能力......"))

    if stockName == "no":
        content = "股票代碼錯誤"
    else:
        content = Msg_fundamental_ability.debt_ability(stockNumber, stockName)

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 獲利能力分析：輸入「獲利能力2330」
elif re.match("獲利能力[0-9]{4}", msg):
    stockNumber = msg.strip("獲利能力")
    stockName = stockprice.get_stock_name(stockNumber)
    line_bot_api.push_message(uid, TextSendMessage(f"正在為您分析股票代號: {stockNumber} 的獲利能力......"))

    if stockName == "no":
        content = "股票代碼錯誤"
    else:
        content = Msg_fundamental_ability.profit_ability(stockNumber, stockName)

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 地雷股健診提示
elif re.match("排除地雷股健診", msg):
    line_bot_api.push_message(uid, TextSendMessage(f"\U0001F538 請輸入地雷股+股票代碼，如「地雷股2002」，即可快速了解該個股是否值得投資!"))
    return 0

# 定存股健診提示
elif re.match("定存股健診", msg):
    line_bot_api.push_message(uid, TextSendMessage(f"\U0001F538 請輸入定存股+股票代碼，如「定存股2002」，即可快速了解該個股是否值得投資!"))
    return 0

# 成長股健診提示
elif re.match("成長股健診", msg):
    line_bot_api.push_message(uid, TextSendMessage(f"\U0001F538 請輸入成長股+股票代碼，如「成長股2002」，即可快速了解該個股是否值得投資!"))
    return 0

# 便宜股健診提示
elif re.match("便宜股健診", msg):
    line_bot_api.push_message(uid, TextSendMessage(f"\U0001F538 請輸入便宜股+股票代碼，如「便宜股2002」，即可快速了解該個股是否值得投資!"))
    return 0
# 地雷股健診（輸入「地雷股2330」）
elif re.match("地雷股[0-9]{4}", msg):
    stockNumber = msg[3:]  # 去掉「地雷股」取代碼
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 正在為您做股票編號: {stockNumber}地雷股排除健診...'))
    stockName = stockprice.get_stock_name(stockNumber)

    if stockName == "no":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤"))
    else:
        content = Msg_diagnose.mine_stock_menu(stockNumber, stockName)
        line_bot_api.push_message(uid, content)
    return 0

# 成長股健診
elif re.match("成長股[0-9]{4}", msg):
    stockNumber = msg[3:]
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 正在為您做股票編號: {stockNumber}成長股健診...'))
    stockName = stockprice.get_stock_name(stockNumber)

    if stockName == "no":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤"))
    else:
        content = Msg_diagnose.growth_stock_menu(stockNumber, stockName)
        line_bot_api.push_message(uid, content)
    return 0

# 定存股健診
elif re.match("定存股[0-9]{4}", msg):
    stockNumber = msg[3:]
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 正在為您做股票編號: {stockNumber} 定存股健診...'))
    stockName = stockprice.get_stock_name(stockNumber)

    if stockName == "no":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤"))
    else:
        content = Msg_diagnose.fixed_deposit_stock_menu(stockNumber, stockName)
        line_bot_api.push_message(uid, content)
    return 0

# 便宜股健診
elif re.match("便宜股[0-9]{4}", msg):
    stockNumber = msg[3:]
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 正在為您做股票編號: {stockNumber} 便宜股健診...'))
    stockName = stockprice.get_stock_name(stockNumber)

    if stockName == "no":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤"))
    else:
        content = Msg_diagnose.cheap_stock_menu(stockNumber, stockName)
        line_bot_api.push_message(uid, content)
    return 0
# ETF 技術面分析，例如：ETF技術面0050
elif re.match('ETF技術面[0-9]', msg):
    stockNumber = msg.strip("ETF技術面")
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 分析ETF編號: {stockNumber}的股價中...'))
    content = Msg_Template.etf_tec_analysis(stockNumber)
    line_bot_api.push_message(uid, content)
    return 0

# ETF 基本面分析，例如：ETF基本面0056
elif re.match('ETF基本面[0-9]', msg):
    stockNumber = msg.strip("ETF基本面")
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 分析ETF編號: {stockNumber}的股價中...'))
    content = Msg_Template.etf_fundation_analysis(stockNumber)
    line_bot_api.push_message(uid, content)
    return 0
# MACD 指標分析，例如：MACD2330
elif re.match("MACD[0-9]", msg):
    stockNumber = msg[4:]
    content = Msg_Template.macd_msg
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 分析ETF編號: {stockNumber} MACD指標...'))
    line_bot_api.push_message(uid, TextSendMessage(content))

    # 呼叫模組產生圖表
    MACD_imgurl = Technical_Analysis.MACD_pic(stockNumber, msg)
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=MACD_imgurl, preview_image_url=MACD_imgurl))

    # 推送相關選項按鈕
    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0

# RSI 指標分析，例如：RSI2330
elif re.match('RSI[0-9]', msg):
    stockNumber = msg[3:]
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 將給您編號{stockNumber} RSI指標...'))

    RSI_imgurl = Technical_Analysis_test.stock_RSI(stockNumber)
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=RSI_imgurl, preview_image_url=RSI_imgurl))

    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0

# BBAND 指標分析，例如：BBAND2330
elif re.match("BBAND[0-9]", msg):
    stockNumber = msg[5:]
    content = Msg_Template.bband_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 將給您編號{stockNumber} BBand指標...'))

    BBANDS_imgurl = Technical_Analysis.BBANDS_pic(stockNumber, msg)
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=BBANDS_imgurl, preview_image_url=BBANDS_imgurl))

    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 三大法人買賣資訊，例如：F2330
elif re.match('F[0-9]', msg):
    stockNumber = msg[1:]
    line_bot_api.push_message(uid, TextSendMessage(f'稍等一下, 將給您編號: {stockNumber}三大法人買賣資訊...'))

    content = Institutional_Investors.institutional_investors(stockNumber)
    line_bot_api.push_message(uid, TextSendMessage(content))

    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 刪除指定股票，例如：刪除2330
elif re.match('刪除[0-9]{4}', msg):
    content = mongodb.delete_my_stock(user_name, msg[2:])
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 清空所有股票清單
elif re.match('清空股票', msg):
    content = mongodb.delete_my_allstock(user_name, uid)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 查詢使用者的股票清單與報價
elif re.match('我的股票', msg):
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 股票查詢中...'))
    content = mongodb.show_my_stock(uid, user_name, msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 查詢股票篩選條件清單
elif re.match('股票清單', msg):
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 股票查詢中...'))
    content = mongodb.show_stock_setting(user_name, uid)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 查詢走勢圖，例如：P2330
elif re.match("P[0-9]{4}", msg):
    stockNumber = msg[1:]
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 股價走勢繪製中...'))

    trend_imgurl = stockprice.stock_trend(stockNumber, msg)
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=trend_imgurl, preview_image_url=trend_imgurl))

    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0

# 查詢 K 線圖，例如：K2330
elif re.match("K[0-9]{4}", msg):
    stockNumber = msg[1:]
    content = Msg_Template.kchart_msg + "\n" + Msg_Template.kd_msg
    line_bot_api.push_message(uid, TextSendMessage(content))
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, K線圖繪製中...'))

    k_imgurl = kchart.draw_kchart(stockNumber)
    if k_imgurl.startswith("https"):
        line_bot_api.push_message(uid, ImageSendMessage(original_content_url=k_imgurl, preview_image_url=k_imgurl))
    else:
        line_bot_api.push_message(uid, TextSendMessage(k_imgurl))

    btn_msg = Msg_Template.stock_reply_other(stockNumber)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 股票籌碼面分析圖，例如：股票籌碼面2330
elif re.match('股票籌碼面[0-9]', msg):
    targetStock = msg[5:]
    line_bot_api.push_message(uid, TextSendMessage(f'分析{targetStock} 籌碼面中，稍等一下。'))

    imgurl2 = Institutional_Investors.institutional_investors_pic(targetStock)
    if imgurl2 == "股票代碼錯誤!":
        line_bot_api.push_message(uid, TextSendMessage("股票代碼錯誤!"))
        return 0

    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=imgurl2, preview_image_url=imgurl2))
    btn_msg = Msg_Template.stock_reply_other(targetStock)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 年收益率分析圖，例如：收益率2330
elif re.match('收益率[0-9]', msg):
    targetStock = msg[3:]
    line_bot_api.push_message(uid, TextSendMessage(f'分析{targetStock}中，稍等一下。'))

    imgurl2 = stockprice.show_return(targetStock, msg)
    line_bot_api.push_message(uid, ImageSendMessage(original_content_url=imgurl2, preview_image_url=imgurl2))

    btn_msg = Msg_Template.stock_reply_other(targetStock)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 查詢特定外幣，例如：外幣USD
elif re.match('外幣[A-Z]{3}', msg):
    currency = msg[2:5]  # 擷取幣別縮寫（例如 USD）
    currency_name = EXRate.getCurrencyName(currency)

    if currency_name == "無可支援的外幣":
        content = "無可支援的外幣"
        line_bot_api.push_message(uid, TextSendMessage(content))
    else:
        line_bot_api.push_message(uid, TextSendMessage(f'您要查詢的外幣是: {currency_name}'))
        text_message = EXRate.showCurrency(currency)
        content = Msg_Exrate.realtime_currency(text_message, currency)
        line_bot_api.push_message(uid, content)
    return 0
# 查看匯率走勢圖，例如：CTUSD
elif re.match("CT[A-Z]{3}", msg):
    currency = msg[2:5]

    if EXRate.getCurrencyName(currency) == "無可支援的外幣":
        line_bot_api.push_message(uid, TextSendMessage('無可支援的外幣'))
        return 0

    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 將會給您匯率走勢圖'))

    # 現金匯率圖（台銀）
    cash_imgurl = EXRate.cash_exrate_sixMonth(currency)
    if cash_imgurl == "現金匯率無資料可分析":
        line_bot_api.push_message(uid, TextSendMessage('現金匯率無資料可分析'))
    else:
        line_bot_api.push_message(uid, ImageSendMessage(original_content_url=cash_imgurl, preview_image_url=cash_imgurl))

    # 即期匯率圖
    spot_imgurl = EXRate.spot_exrate_sixMonth(currency)
    if spot_imgurl == "即期匯率無資料可分析":
        line_bot_api.push_message(uid, TextSendMessage('即期匯率無資料可分析'))
    else:
        line_bot_api.push_message(uid, ImageSendMessage(original_content_url=spot_imgurl, preview_image_url=spot_imgurl))

    # 顯示其他操作選單
    btn_msg = Msg_Exrate.realtime_currency_other(currency)
    line_bot_api.push_message(uid, btn_msg)
    return 0
# 台幣買入外幣，例如：買入外幣USD1000
elif re.match("買入外幣[A-Z]{3}[0-9]", msg):
    currency = msg[4:7]
    currency_name = EXRate.getCurrencyName(currency)

    if currency_name == "無可支援的外幣":
        content = "無可支援的外幣"
    else:
        line_bot_api.push_message(uid, TextSendMessage("正在為您做外幣換算......"))
        content = EXRate.exchange_currency(msg)

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 台幣賣出換回外幣
elif re.match("賣出外幣[A-Z]{3}[0-9]", msg):
    currency = msg[4:7]
    currency_name = EXRate.getCurrencyName(currency)

    if currency_name == "無可支援的外幣":
        content = "無可支援的外幣"
    else:
        line_bot_api.push_message(uid, TextSendMessage("正在為您做外幣換算......"))
        content = EXRate.exchange_currency(msg)

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 新增外幣提醒設定，例如：新增外幣USD>32
elif re.match('新增外幣[A-Z]{3}', msg):
    currency = msg[4:7]
    currency_name = EXRate.getCurrencyName(currency)

    if currency_name == "無可支援的外幣":
        content = "無可支援的外幣"
    elif re.match('新增外幣[A-Z]{3}[<>][0-9]', msg):  # 有設定條件
        content = mongodb.write_my_currency(uid, user_name, currency, msg[7:8], msg[8:])
    else:
        content = mongodb.write_my_currency(uid, user_name, currency, "未設定", "未設定")

    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 刪除外幣提醒，例如：刪除外幣USD
elif re.match('刪除外幣[A-Z]{3}', msg):
    content = mongodb.delete_my_currency(user_name, msg[4:7])
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 清空所有外幣提醒
elif re.match('清空外幣', msg):
    content = mongodb.delete_my_allcurrency(user_name, uid)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 查詢自選外幣目前匯率
elif re.match('我的外幣', msg):
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 匯率查詢中...'))
    content = mongodb.show_my_currency(uid, user_name)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0

# 查詢外幣設定的提醒條件清單
elif re.match('外幣清單', msg):
    line_bot_api.push_message(uid, TextSendMessage('稍等一下, 外幣查詢中...'))
    content = mongodb.show_currency_setting(user_name, uid)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
# 外幣兌換功能，例如：換匯USD/JPY
elif re.match("換匯[A-Z]{3}/[A-Z{3}]", msg):
    line_bot_api.push_message(uid, TextSendMessage("將為您做外匯計算....."))
    content = EXRate.getExchangeRate(msg)
    line_bot_api.push_message(uid, TextSendMessage(content))
    return 0
