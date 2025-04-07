# news.py
import requests
from bs4 import BeautifulSoup

happy = u'\U0001F604'
emoji_list = [u'\U0001F4D5', u'\U0001F606']

def get_single_stock_news(stockNumber):
    try:
        url = f'https://tw.stock.yahoo.com/quote/{stockNumber}/news'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[log:ERROR] Failed to fetch page for {stockNumber}: HTTP {response.status_code}")
            return ["無法獲取新聞"], []
        
        sp = BeautifulSoup(response.text, "html.parser")
        articles = sp.find_all('h3', class_='Mt(0)')  # Yahoo Finance 新聞標題的典型類
        if not articles:
            print(f"[log:ERROR] No news articles found for {stockNumber}")
            return ["無法獲取新聞"], []
        
        title_list = []
        url_list = []
        for i in range(min(len(articles), 5)):  # 前五則新聞
            article = articles[i].find('a')
            if article:
                title = article.text.strip()
                if len(title) > 20:
                    title = title[:20]
                title_list.append(title)
                href = article.get('href')
                if href.startswith('http'):
                    url_list.append(href)
                else:
                    url_list.append(f'https://tw.stock.yahoo.com{href}')
        
        if not title_list:
            print(f"[log:ERROR] No valid news links found for {stockNumber}")
            return ["無法獲取新聞"], []
        
        return title_list, url_list
    except Exception as e:
        print(f"[log:ERROR] Error fetching news for {stockNumber}: {e}")
        return ["無法獲取新聞"], []

# 其他函數保持不變...
