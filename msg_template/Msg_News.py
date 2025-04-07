# Msg_News.py
from linebot.models import FlexSendMessage, TextSendMessage
import news

def single_stock(stockNumber):
    start_url = "https://tw.stock.yahoo.com"
    title_list, url_list = news.get_single_stock_news(stockNumber)
    
    # 檢查是否獲取到有效新聞
    if not url_list or title_list[0] == "無法獲取新聞":
        return TextSendMessage(text=f"無法獲取 {stockNumber} 的新聞數據，請稍後再試！")
    
    # 動態構建按鈕
    buttons = []
    for i in range(min(len(title_list), 5)):  # 最多 5 則新聞
        buttons.append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": title_list[i],
                "uri": start_url + url_list[i]
            }
        })
    buttons.append({"type": "spacer", "size": "sm"})
    
    flex_message = FlexSendMessage(
        alt_text="個股新聞",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/uvrIuT9.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit",
                "position": "relative",
                "margin": "none"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "財金新聞",
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": buttons,
                "flex": 0
            }
        }
    )
    return flex_message

def exrate_news():
    start_url = "https://news.cnyes.com"
    title_list, url_list = news.anue_forex_news()
    
    # 檢查是否獲取到有效新聞
    if not url_list or title_list[0] == "無法獲取外幣匯率新聞":
        return TextSendMessage(text="無法獲取外幣匯率新聞，請稍後再試！")
    
    buttons = []
    for i in range(min(len(title_list), 5)):  # 最多 5 則新聞
        buttons.append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": title_list[i],
                "uri": url_list[i]  # 已包含完整 URL
            }
        })
    buttons.append({"type": "spacer", "size": "sm"})
    
    flex_message = FlexSendMessage(
        alt_text="外匯新聞",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/uvrIuT9.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "fit",
                "position": "relative",
                "margin": "none"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "外匯新聞",
                        "weight": "bold",
                        "size": "xl",
                        "style": "normal"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": buttons,
                "flex": 0
            }
        }
    )
    return flex_message

def weekly_finance_news():
    img, url = news.weekly_news()
    
    # 檢查是否獲取到有效數據
    if "無法獲取" in img or "無法獲取" in url:
        return TextSendMessage(text="無法獲取每周財經大事新聞，請稍後再試！")
    
    flex_message = FlexSendMessage(
        alt_text="每周財經大事新聞",
        contents={
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": img,
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "1252:837",
                        "gravity": "center",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": url
                        }
                    }
                ],
                "paddingAll": "0px"
            }
        }
    )
    return flex_message
