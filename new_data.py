import pandas as pd

# Load price data
tickers = ['AAPL', 'GOOG', 'MSFT', 'IBM']
price_data = {}

for ticker in tickers:
    df = pd.read_csv(f'dataset/{ticker}_price_data.csv', parse_dates=['Date'])
    df = df[['Date', 'Close']]
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')  # <-- force numeric, set invalids to NaN
    df = df.rename(columns={'Close': ticker})
    price_data[ticker] = df

# Merge all price data on Date
df_merged = price_data['AAPL']
for ticker in tickers[1:]:
    df_merged = df_merged.merge(price_data[ticker], on='Date')

df_merged = df_merged.dropna()

# Portfolio weights
portfolios = {
    1: {'AAPL': 0.25, 'GOOG': 0.25, 'MSFT': 0.25, 'IBM': 0.25},
    2: {'AAPL': 0.20, 'GOOG': 0.26, 'MSFT': 0.20, 'IBM': 0.15},
    3: {'AAPL': 0.22, 'GOOG': 0.30, 'MSFT': 0.32, 'IBM': 0.20},
}

# Calculate portfolio values
final_df = pd.DataFrame()

for pid, weights in portfolios.items():
    df_port = df_merged.copy()
    df_port['portfolio_value'] = 0

    for ticker in tickers:
        df_port['portfolio_value'] += df_port[ticker] * weights[ticker]

    df_port['portfolio_id'] = pid
    final_df = pd.concat([final_df, df_port[['Date', 'portfolio_value', 'portfolio_id']]])

# Save to CSV
final_df.rename(columns={'Date': 'trade_date'}, inplace=True)
final_df.to_csv("new_portfolio_daily_value.csv", index=False)
print("✅ Generated new_portfolio_daily_value.csv")
