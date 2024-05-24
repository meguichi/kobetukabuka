import streamlit as st
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# Streamlitの設定
st.title('Stock Analysis App')
st.sidebar.header('User Input')

# ユーザー入力
ticker_info = st.sidebar.text_input('Ticker Symbol (e.g., 4755 for 4755.T)', '1489')
ticker_info = ticker_info + '.T'


start_date = st.sidebar.date_input('Start Date', datetime.date(2015, 1, 1))
end_date = datetime.datetime.now()
erea = st.sidebar.slider('Days of Data to Display', 10, 100, 15)

# 株価データの取得
df = yf.download(ticker_info, start=start_date, end=end_date)

# トレンドラインの追加
def add_trendline(df):
    x = np.arange(len(df))
    y = df['Close']
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    line = slope * x + intercept
    return line

df['trendline'] = add_trendline(df)

# 移動平均の計算
df['sma25'] = df['Close'].rolling(window=25).mean()
df['sma75'] = df['Close'].rolling(window=75).mean()
df['sma200'] = df['Close'].rolling(window=200).mean()

# 価格差の計算
df['change'] = df['Close'] - df['Close'].shift(1)

# ラグ指標の計算
for i in range(1, 6):
    df[f'Lag_{i}'] = df['Close'] - df['Close'].shift(i)

# MACDの計算
ema12 = df['Close'].ewm(span=12).mean()
ema26 = df['Close'].ewm(span=26).mean()
macd = ema12 - ema26
signal = macd.ewm(span=9).mean()
histogram = macd - signal

# RSIの計算
n = 14
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=n).mean()
avg_loss = loss.rolling(window=n).mean()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# グラフの描画
def plot_moving_average():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Close'][-erea:], label='Close')
    ax.plot(df['sma25'][-erea:], label='SMA25')
    ax.plot(df['sma75'][-erea:], label='SMA75')
    ax.plot(df['sma200'][-erea:], label='SMA200')
    ax.legend(loc='best')
    ax.set_title('Moving Average')
    st.pyplot(fig)

def plot_macd():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(macd[-erea:], label='MACD')
    ax.plot(signal[-erea:], label='Signal')
    ax.bar(histogram.index[-erea:], histogram[-erea:], label='Histogram', width=0.8)
    ax.legend(loc='best')
    ax.set_title('MACD')
    st.pyplot(fig)

def plot_rsi():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(rsi[-erea:], label='RSI')
    ax.axhline(y=70, color='red', linestyle='--')
    ax.axhline(y=30, color='red', linestyle='--')
    ax.legend(loc='best')
    ax.set_title('RSI')
    st.pyplot(fig)

# Google AdSenseの所有権確認用メタタグ
st.markdown(
    """
    <meta name="google-adsense-account" content="ca-pub-5375032594935578" />
    """,
    unsafe_allow_html=True
)



<meta name="google-adsense-account" content="ca-pub-5375032594935578">

ad_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5375032594935578"
     crossorigin="anonymous"></script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""
# グラフの表示
st.header(f'Stock Analysis for {ticker_info}')
plot_moving_average()
plot_macd()
plot_rsi()
