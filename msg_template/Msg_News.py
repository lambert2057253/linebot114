from linebot.models import FlexSendMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import news

def single_stock(stockNumber):
    start_url = "https://tw.stock.yahoo.com"
    title_list, url_list = news.get_single_stock_news(stockNumber)
    
    # 檢查是否獲取到有效新聞
    if not url_list or title_list[0] == "無法獲取新聞":
        return TextSendMessage(text=f"無法獲取 {stockNumber} 的新聞數據，請稍後再試！")
    
    # 動態構建新聞內容（body）和按鈕（footer）
    news_items = []
    buttons = []
    for i in range(min(len(title_list), 5)):  # 最多 5 則新聞
        # 確保 title 和 url 有效
        title = title_list[i] if title_list[i] and isinstance(title_list[i], str) else "無標題"
        url = url_list[i] if url_list[i] and isinstance(url_list[i], str) else ""
        
        # 如果 URL 無效，跳過這條新聞
        if not url:
            continue
        
        # 截斷標題（body 顯示用）
        display_title = title[:37] + "..." if len(title) > 37 else title
        # 截斷標題（按鈕標籤用，Line 按鈕標籤最多 40 字元）
        button_label = title[:37] + "..." if len(title) > 37 else title
        
        url = start_url + url if not url.startswith("http") else url
        
        # 添加新聞標題到 body
        news_items.append({
            "type": "text",
            "text": display_title,
            "size": "sm",
            "color": "#555555",
            "wrap": True,
            "margin": "md"
        })
        # 添加分隔線（如果不是最後一則新聞）
        if i < min(len(title_list), 5) - 1:
            news_items.append({
                "type": "separator",
                "margin": "md"
            })
        
        # 添加按鈕到 footer，使用新聞標題作為按鈕標籤
        button = {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": button_label,  # 直接使用新聞標題
                "uri": url
            }
        }
        buttons.append(button)
    
    # 如果沒有有效新聞，返回簡單消息
    if not news_items or not buttons:
        return TextSendMessage(text=f"無法獲取 {stockNumber} 的有效新聞數據，請稍後再試！")
    
    # 檢查 buttons 是否有效
    if not buttons:
        return TextSendMessage(text=f"無法生成 {stockNumber} 的新聞按鈕，請稍後再試！")
    
    # 構建 Flex Message
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
                    },
                    #*news_items
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
    
    # 快速回覆
    quick_reply = TextSendMessage(
        text=f"目前找到 {len(buttons)} 則新聞，是否想知道更多？",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="即時股價", text=f"#{stockNumber}")),
                QuickReplyButton(action=MessageAction(label="關注", text=f"關注{stockNumber}")),
                QuickReplyButton(action=MessageAction(label="新聞", text=f"N{stockNumber}")),
            ]
        )
    )
    
    return [flex_message, quick_reply]
    
def exrate_news():
    start_url = "https://news.cnyes.com"
    title_list, url_list = news.anue_forex_news()
    
    if not url_list or title_list[0] == "無法獲取外匯新聞":
        return TextSendMessage(text="無法獲取外匯新聞，請稍後再試！")
    
    news_items = []
    buttons = []
    for i in range(min(len(title_list), 5)):
        title = title_list[i][:37] + "..." if len(title_list[i]) > 37 else title_list[i]
        url = url_list[i]  # 已包含完整 URL
        
        news_items.append({
            "type": "text",
            "text": title,
            "size": "sm",
            "color": "#555555",
            "wrap": True,
            "margin": "md"
        })
        if i < min(len(title_list), 5) - 1:
            news_items.append({
                "type": "separator",
                "margin": "md"
            })
        
        buttons.append({
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": f"閱讀全文 {i+1}",
                "uri": url
            }
        })
    buttons.append({"type": "spacer", "size": "sm"})
    
    flex_message = FlexSendMessage(
        alt_text="外匯新聞",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/forex_image.jpg",  # 替換為外匯相關圖片
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
                    },
                    *news_items
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
    
    quick_reply = TextSendMessage(
        text="想知道更多？",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="外匯新聞", text="/外匯新聞")),
                QuickReplyButton(action=MessageAction(label="頭條新聞", text="/頭條新聞")),
            ]
        )
    )
    
    return [flex_message, quick_reply]

def weekly_finance_news():
    img, url = news.weekly_news()
    
    if "無法獲取" in img or "無法獲取" in url:
        return TextSendMessage(text="無法獲取每周財經大事新聞，請稍後再試！")
    
    flex_message = FlexSendMessage(
        alt_text="每周財經大事新聞",
        contents={
            "type": "bubble",
            "size": "kilo",  # 調整為較小尺寸
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
                    },
                    {
                        "type": "text",
                        "text": "每周財經大事",
                        "weight": "bold",
                        "size": "md",
                        "margin": "md",
                        "color": "#555555"
                    }
                ],
                "paddingAll": "0px"
            }
        }
    )
    
    quick_reply = TextSendMessage(
        text="想知道更多？",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="每周財經大事", text="/每周財經大事")),
                QuickReplyButton(action=MessageAction(label="頭條新聞", text="/頭條新聞")),
            ]
        )
    )
    
    return [flex_message, quick_reply]
