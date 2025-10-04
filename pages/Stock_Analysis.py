import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import (
    plotly_table, candlestick, RSI, MACD,
    Moving_average, close_chart
)

# Setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📄",
    layout="wide"
)
st.title("Stock Analysis")
col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker_symbol = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_data = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_data = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker_symbol)

# Create Ticker object
stock = yf.Ticker(ticker_symbol)

# Safe way to get stock info with fallback values
def get_stock_info(info_dict, key, default="N/A"):
    return info_dict.get(key, default)

# Display basic company information
try:
    st.write(get_stock_info(stock.info, 'longBusinessSummary', 'Business summary not available'))
    st.write("**Sector:**", get_stock_info(stock.info, 'sector'))
    st.write("**Full Time Employees:**", get_stock_info(stock.info, 'fullTimeEmployees'))
    st.write("**Website:**", get_stock_info(stock.info, 'website'))
except Exception as e:
    st.error(f"Error fetching basic stock information: {e}")

col1, col2 = st.columns(2)

with col1:
    try:
        market_cap = get_stock_info(stock.info, "marketCap", "N/A")
        beta = get_stock_info(stock.info, "beta", "N/A")
        trailing_eps = get_stock_info(stock.info, "trailingEPS", "N/A")
        trailing_pe = get_stock_info(stock.info, "trailingPE", "N/A")

        if isinstance(market_cap, (int, float)):
            if market_cap >= 1e12:
                market_cap = f"${market_cap/1e12:.2f}T"
            elif market_cap >= 1e9:
                market_cap = f"${market_cap/1e9:.2f}B"
            elif market_cap >= 1e6:
                market_cap = f"${market_cap/1e6:.2f}M"
            else:
                market_cap = f"${market_cap:,.0f}"

        if isinstance(beta, (int, float)):
            beta = f"{beta:.2f}"

        if isinstance(trailing_eps, (int, float)):
            trailing_eps = f"${trailing_eps:.2f}"

        if isinstance(trailing_pe, (int, float)):
            trailing_pe = f"{trailing_pe:.2f}"

        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df[''] = [market_cap, beta, trailing_eps, trailing_pe]

        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error creating financial metrics table: {e}")

with col2:
    try:
        df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margin', 'Debt to Equity', 'Return on Equity'])
        df[''] = [
            get_stock_info(stock.info, "quickRatio"),
            get_stock_info(stock.info, "revenuePerShare"),
            get_stock_info(stock.info, "profitMargins"),
            get_stock_info(stock.info, "debtToEquity"),
            get_stock_info(stock.info, "returnOnEquity")
        ]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating financial ratios table: {e}")

# Download price data
data = yf.download(ticker_symbol, start=start_data, end=end_data)

col1, col2, col3 = st.columns(3)

current_price = float(data['Close'].iloc[-1])
previous_price = float(data['Close'].iloc[-2])
daily_change = current_price - previous_price

with col1:
    st.metric(
        label=f"{ticker_symbol} Price",
        value=f"${current_price:.2f}",
        delta=f"{daily_change:.2f}"
    )

last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)
st.write('##### Historical Data (Last 10 days)')
st.plotly_chart(fig_df, use_container_width=True)

# Timeframe buttons
col1, col2, col3, col4, col5, col6, col7 = st.columns([1]*7)
num_period = ''

with col1:
    if st.button('5D'): num_period = '5d'
with col2:
    if st.button('1M'): num_period = '1mo'
with col3:
    if st.button('6M'): num_period = '6mo'
with col4:
    if st.button('YTD'): num_period = 'ytd'
with col5:
    if st.button('1Y'): num_period = '1y'
with col6:
    if st.button('5Y'): num_period = '5y'
with col7:
    if st.button('MAX'): num_period = 'max'

# Chart settings
col1, col2, col3 = st.columns([1,1,4])

with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

# Get historical data for charts
chart_data = stock.history(period='max')

if num_period == '':
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(chart_data, '1y'), use_container_width=True)
        st.plotly_chart(RSI(chart_data, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(chart_data, '1y'), use_container_width=True)
        st.plotly_chart(MACD(chart_data, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(chart_data, '1y'), use_container_width=True)
        st.plotly_chart(RSI(chart_data, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(chart_data, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(chart_data, '1y'), use_container_width=True)
        st.plotly_chart(MACD(chart_data, '1y'), use_container_width=True)

else:
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(chart_data, num_period), use_container_width=True)
        st.plotly_chart(RSI(chart_data, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(chart_data, num_period), use_container_width=True)
        st.plotly_chart(MACD(chart_data, num_period), use_container_width=True)
