import pandas as pd
import os

tickers = ['AAPL', 'GOOG', 'MSFT', 'IBM']
weights = {'AAPL': 0.25, 'GOOG': 0.25, 'MSFT': 0.25, 'IBM': 0.25}
price_data = {}

# Load all CSVs
for ticker in tickers:
    filepath = f"dataset/{ticker}_price_data.csv"
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df = df[['Date', 'Close']].rename(columns={'Close': ticker})
    price_data[ticker] = df

# Merge all dataframes on Date
merged_df = None
for df in price_data.values():
    merged_df = df if merged_df is None else pd.merge(merged_df, df, on='Date', how='outer')

# Clean and calculate portfolio value
merged_df = merged_df.sort_values('Date').dropna()
merged_df['portfolio_value'] = sum(merged_df[t] * weights[t] for t in tickers)

# Prepare final table
portfolio_id = 1
final_df = merged_df[['Date', 'portfolio_value']].copy()
final_df['portfolio_id'] = portfolio_id
final_df.columns = ['trade_date', 'portfolio_value', 'portfolio_id']
final_df = final_df[['portfolio_id', 'trade_date', 'portfolio_value']]

# Preview result
print(final_df.head())

# Optional: Save to CSV
final_df.to_csv("new_portfolio_daily_value.csv", index=False)
