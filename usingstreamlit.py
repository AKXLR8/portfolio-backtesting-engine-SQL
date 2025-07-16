# streamlit_app.py
import streamlit as st
import pandas as pd
import psycopg2

conn = psycopg2.connect("postgresql://neondb_owner:npg_VfmpQuI3rWK1@ep-dark-forest-a16bt9bq-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

df = pd.read_sql("SELECT * FROM portfolio_metrics", conn)

st.title("Portfolio Metrics Dashboard")
st.dataframe(df)

st.subheader("Sharpe Ratio (x10 for visibility)")
st.line_chart(df.set_index("portfolio_id")["sharpe_ratio"] * 10)

st.subheader("Annual Return (%)")
st.bar_chart(df.set_index("portfolio_id")["annual_return"])

st.subheader("Annual Volatility (%)")
st.bar_chart(df.set_index("portfolio_id")["annual_volatility"])

