import streamlit as st
import pandas as pd
from pages.utils.model_train import (
    get_data, stationary_check, get_rolling_mean,
    get_differencing_order, fit_model, evaluate_model,
    scaling, get_forecast, inverse_scaling
)
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(page_title='Stock Prediction', page_icon='chart_with_downwards_trend', layout='wide')
st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**", rmse)

# ✅ get_forecast now returns forecast_df
forecast = get_forecast(scaled_data, differencing_order)

# ✅ inverse scaling per column
forecast['Close'] = inverse_scaling(scaler, forecast['Close']).flatten()

st.write('#### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])
st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)
