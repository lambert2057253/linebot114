# Technical_Analysis_test.py
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import Imgur

# 設定顏色
color = ['#2196f3', '#4caf50', '#ffc107', '#f436c7', '#f27521', '#e00b0b']

def TheConstructor(userstock):
    start = datetime.datetime.now() - datetime.timedelta(days=365)
    end = datetime.date.today()
    
    pd.core.common.is_list_like = pd.api.types.is_list_like
    yf.pdr_override()
    
    try:
        stock = data.get_data_yahoo(userstock + '.TW', start, end)
    except:
        stock = 'https://i.imgur.com/RFmkvQX.jpg'
    
    return stock

# 股票K線圖
def stock_Candlestick(userstock):
    stock = TheConstructor(userstock)
    
    if isinstance(stock, str):
        return stock
    
    fig = plt.figure(figsize=(24, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(range(0, len(stock.index), 5))
    ax.set_xticklabels(stock.index[::5])
    plt.xticks(fontsize=10, rotation=90)
    
    # 手動繪製K線圖（替代 mpl_finance）
    for i in range(len(stock)):
        open_price = stock['Open'].iloc[i]
        close_price = stock['Close'].iloc[i]
        high_price = stock['High'].iloc[i]
        low_price = stock['Low'].iloc[i]
        color_candle = 'r' if close_price >= open_price else 'g'
        ax.plot([i, i], [low_price, high_price], color=color_candle, linewidth=1)
        ax.plot([i, i], [open_price, close_price], color=color_candle, linewidth=3)
    
    plt.title("Candlestick Chart")
    plt.grid(True, axis='y')
    plt.savefig('Candlestick_chart.png')
    plt.close()
    
    return Imgur.showImgur('Candlestick_chart')

# KD指標
def stock_KD(userstock):
    stock = TheConstructor(userstock)
    
    if isinstance(stock, str):
        return stock
    
    # 手動計算 KD (Stochastic Oscillator)
    period = 9
    low_min = stock['Low'].rolling(window=period).min()
    high_max = stock['High'].rolling(window=period).max()
    k = 100 * (stock['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(window=3).mean()
    
    ret = pd.DataFrame({'K': k, 'D': d}, index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('KD')
    plt.grid(True, axis='y')
    plt.savefig('KD.png')
    plt.close()
    return Imgur.showImgur('KD')

# 移動平均線（Moving Average）
def stock_MA(userstock):
    stock = TheConstructor(userstock)
    
    if isinstance(stock, str):
        return stock
    
    ret = pd.DataFrame({
        '10-day average': stock['Close'].rolling(window=10).mean(),
        '20-day average': stock['Close'].rolling(window=20).mean(),
        '60-day average': stock['Close'].rolling(window=60).mean()
    }, index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Moving_Average')
    plt.grid(True, axis='y')
    plt.savefig('Moving_Average.png')
    plt.close()
    return Imgur.showImgur('Moving_Average')

# MACD
def stock_MACD(userstock):
    stock = TheConstructor(userstock)
    ret = pd.DataFrame()
    
    if isinstance(stock, str):
        return stock
    
    ema12 = stock['Close'].ewm(span=12, adjust=False).mean()
    ema26 = stock['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - signal
    ret['MACD'] = macd
    ret['MACDsignal'] = signal
    ret['MACDhist'] = macd_hist
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('MACD')
    plt.grid(True, axis='y')
    plt.savefig('MACD.png')
    plt.close()
    return Imgur.showImgur('MACD')

# OBV (On Balance Volume)
def stock_OBV(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    # 手動計算 OBV
    obv = [0]  # 初始值
    for i in range(1, len(stock)):
        if stock['Close'].iloc[i] > stock['Close'].iloc[i-1]:
            obv.append(obv[-1] + stock['Volume'].iloc[i])
        elif stock['Close'].iloc[i] < stock['Close'].iloc[i-1]:
            obv.append(obv[-1] - stock['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    ret = pd.DataFrame(obv, index=stock.index, columns=['OBV'])
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('On_Balance_Volume')
    plt.grid(True, axis='y')
    plt.savefig('On_Balance_Volume.png')
    plt.close()
    return Imgur.showImgur('On_Balance_Volume')

# Williams %R
def stock_William(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    # 手動計算 Williams %R
    period = 14
    high_max = stock['High'].rolling(window=period).max()
    low_min = stock['Low'].rolling(window=period).min()
    williams = -100 * (high_max - stock['Close']) / (high_max - low_min)
    ret = pd.DataFrame(williams, columns=['Williams'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Williams_Overbought')
    plt.grid(True, axis='y')
    plt.savefig('Williams_Overbought.png')
    plt.close()
    return Imgur.showImgur('Williams_Overbought')

# ATR (Average True Range)
def stock_ATR(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    # 手動計算 ATR
    tr = pd.DataFrame({
        'HL': stock['High'] - stock['Low'],
        'HC': abs(stock['High'] - stock['Close'].shift()),
        'LC': abs(stock['Low'] - stock['Close'].shift())
    }).max(axis=1)
    atr = tr.rolling(window=14).mean()
    ret = pd.DataFrame(atr, columns=['Average True Range'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Average_True_Range')
    plt.grid(True, axis='y')
    plt.savefig('Average_True_Range.png')
    plt.close()
    return Imgur.showImgur('Average_True_Range')

# ADX (Average Directional Indicator)
def stock_ADX(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    # 手動計算 ADX（簡化版，使用 +DI 和 -DI 的平均）
    tr = pd.DataFrame({
        'HL': stock['High'] - stock['Low'],
        'HC': abs(stock['High'] - stock['Close'].shift()),
        'LC': abs(stock['Low'] - stock['Close'].shift())
    }).max(axis=1)
    dm_plus = (stock['High'] - stock['High'].shift()).where(lambda x: x > 0, 0)
    dm_minus = (stock['Low'].shift() - stock['Low']).where(lambda x: x > 0, 0)
    atr = tr.rolling(window=14).mean()
    di_plus = 100 * dm_plus.rolling(window=14).mean() / atr
    di_minus = 100 * dm_minus.rolling(window=14).mean() / atr
    dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
    adx = dx.rolling(window=14).mean()
    ret = pd.DataFrame(adx, columns=['Average Directional Indicator'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Average_Directional_Indicator')
    plt.grid(True, axis='y')
    plt.savefig('Average_Directional_Indicator.png')
    plt.close()
    return Imgur.showImgur('Average_Directional_Indicator')

# RSI
def stock_RSI(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    delta = stock['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=6).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=6).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    ret = pd.DataFrame(rsi, columns=['Relative Strength Index'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title(userstock + ' RSI')
    plt.grid(True, axis='y')
    plt.savefig('Relative_Strength_Index.png')
    plt.close()
    return Imgur.showImgur('Relative_Strength_Index')

# MFI (Money Flow Index)
def stock_MFI(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    typical_price = (stock['High'] + stock['Low'] + stock['Close']) / 3
    money_flow = typical_price * stock['Volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(), 0).rolling(window=14).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(), 0).rolling(window=14).sum()
    mfr = positive_flow / negative_flow
    mfi = 100 - (100 / (1 + mfr))
    ret = pd.DataFrame(mfi, columns=['Money Flow Index'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Money_Flow_Index')
    plt.grid(True, axis='y')
    plt.savefig('Money_Flow_Index.png')
    plt.close()
    return Imgur.showImgur('Money_Flow_Index')

# ROC (Rate of Change)
def stock_ROC(userstock):
    stock = TheConstructor(userstock)
    if isinstance(stock, str):
        return stock
    
    roc = ((stock['Close'] - stock['Close'].shift(10)) / stock['Close'].shift(10)) * 100
    ret = pd.DataFrame(roc, columns=['Receiver Operating Characteristic Curve'], index=stock.index)
    ret = pd.concat([ret, stock['Close']], axis=1)
    
    ret.plot(color=color, linestyle='dashed')
    ret['Close'].plot(secondary_y=True, color=color[5])
    plt.title('Receiver_Operating_Characteristic_Curve')
    plt.grid(True, axis='y')
    plt.savefig('Receiver_Operating_Characteristic_Curve.png')
    plt.close()
    return Imgur.showImgur('Receiver_Operating_Characteristic_Curve')
