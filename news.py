'''
emoji編碼列表：
https://apps.timwhitlock.info/emoji/tables/unicode#block-6c-other-additional-symbols
'''
import requests
from bs4 import BeautifulSoup
from cachetools import TTLCache
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Emoji 定義
HAPPY = u'\U0001F604'  # 笑臉
BOOK = u'\U0001F4D5'   # 書本
LAUGH = u'\U0001F606'  # 笑聲
EMOJI_LIST = [BOOK, LAUGH]

# 緩存設置（1 小時）
cache = TTLCache(maxsize=100, ttl=3600)

# 通用函數：截斷標題（考慮中文多字節）
def truncate_title(title, max_len=20):
    if len(title) > max_len:
        return title[:max_len] + "..."
    return title

# 通用請求函數
def fetch_url(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"網絡請求失敗: {url}, 錯誤: {e}")
        return None

# 1. 個股新聞（Yahoo Finance）
def get_single_stock_news(stock_number):
    if stock_number in cache:
        return cache[stock_number]
    
    url = f'https://tw.stock.yahoo.com/quote/{stock_number}/news'  # 使用新版 URL
    sp = fetch_url(url)
    if not sp:
        return ["無法獲取新聞"], []
    
    try:
        articles = sp.select('.news-list li a')  # 使用 CSS 選擇器
        if not articles:
            logging.warning(f"未找到新聞列表: {stock_number}")
            return ["無新聞數據"], []
        
        title_list, url_list = [], []
        for article in articles[:5]:  # 前 5 則
            title = truncate_title(article.text.strip())
            title_list.append(title)
            url_list.append(article['href'])
        
        cache[stock_number] = (title_list, url_list)
        return title_list, url_list
    except Exception as e:
        logging.error(f"解析個股新聞失敗: {stock_number}, 錯誤: {e}")
        return ["解析錯誤"], []

# 2. 鉅亨網外匯新聞
def anue_forex_news():
    cache_key = "anue_forex_news"
    if cache_key in cache:
        return cache[cache_key]
    
    url = 'https://news.cnyes.com/news/cat/forex'
    sp = fetch_url(url)
    if not sp:
        return ["無法獲取外匯新聞"], []
    
    try:
        articles = sp.find_all('a', class_='_1Zdp')
        if not articles:
            logging.warning("未找到外匯新聞")
            return ["無外匯新聞"], []
        
        title_list, url_list = [], []
        for article in articles[:5]:
            title = truncate_title(article.get('title', '無標題'))
            title_list.append(title)
            url_list.append('https://news.cnyes.com' + article.get('href', ''))
        
        cache[cache_key] = (title_list, url_list)
        return title_list, url_list
    except Exception as e:
        logging.error(f"解析外匯新聞失敗: {e}")
        return ["解析錯誤"], []

# 3. 鉅亨網頭條新聞
def anue_headline_news():
    cache_key = "anue_headline_news"
    if cache_key in cache:
        return cache[cache_key]
    
    url = 'https://news.cnyes.com/news/cat/headline'
    sp = fetch_url(url)
    if not sp:
        return "無法獲取頭條新聞"
    
    try:
        articles = sp.find_all('a', class_='_1Zdp')
        if not articles:
            logging.warning("未找到頭條新聞")
            return "無頭條新聞"
        
        content = ""
        for article in articles[:5]:
            title = article.get('title', '無標題')
            href = 'https://news.cnyes.com' + article.get('href', '')
            content += f"{title}\n{href}\n------\n"
        
        cache[cache_key] = content
        return content
    except Exception as e:
        logging.error(f"解析頭條新聞失敗: {e}")
        return "解析錯誤"

# 4. 每週財經大事（Pocketmoney）
def weekly_news():
    cache_key = "weekly_news"
    if cache_key in cache:
        return cache[cache_key]
    
    url = 'https://pocketmoney.tw/articles/'
    sp = fetch_url(url)
    if not sp:
        return "無法獲取財經大事", ""
    
    try:
        img = sp.find('img', class_="wp-post-image")
        link = sp.find('a', class_='post-thumb')
        if not img or not link:
            logging.warning("未找到財經大事圖片或連結")
            return "無圖片", "無連結"
        
        img_url = img.get("src", "")
        href = link.get('href', "")
        cache[cache_key] = (img_url, href)
        return img_url, href
    except Exception as e
