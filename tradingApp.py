import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "chart_with_downward_trend:",
    layout="wide"
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide a platform for you to collect all information prior to investigation prior to investing in stocks.")

st.image("app.png")

st.markdown("## We provide trhe following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the info regarding stocks. ")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting  models.")

st.markdown("#### :three: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stock assets based on their risk by relating the stock’s beta (systematic risk) to the risk-free rate and the expected market return.")

st.markdown("#### :four: CAPM Beta")
st.write("Calcualtes Beta and Expected Return for Individual Stocks.")