import yfinance as yf
import os

tickers = ['AAPL', 'GOOG', 'MSFT', 'IBM']
start = '2015-01-01'
end = '2015-12-31'

os.makedirs("dataset", exist_ok=True)

for ticker in tickers:
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)  # <== This adds the Date column
    data.to_csv(f"dataset/{ticker}_price_data.csv", index=False)
