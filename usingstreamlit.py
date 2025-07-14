# streamlit_app.py
import streamlit as st
import pandas as pd
import psycopg2

# Connect to your PostgreSQL DB
conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)

df = pd.read_sql("SELECT * FROM portfolio_metrics", conn)

st.title("Portfolio Metrics Dashboard")
st.dataframe(df)

st.subheader("Sharpe Ratio (x10 for visibility)")
st.line_chart(df.set_index("portfolio_id")["sharpe_ratio"] * 10)

st.subheader("Annual Return (%)")
st.bar_chart(df.set_index("portfolio_id")["annual_return"])

st.subheader("Annual Volatility (%)")
st.bar_chart(df.set_index("portfolio_id")["annual_volatility"])

