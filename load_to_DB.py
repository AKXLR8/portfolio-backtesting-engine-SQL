import psycopg2
import pandas as pd
import os

conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)

curr = conn.cursor()
tickers = pd.read_csv("dataset/tickers.csv")


def insert_asset(ticker):
    curr.execute(
        """INSERT INTO assets(ticker, name, asset_type, currency)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (ticker) DO NOTHING""",
        (ticker, f"{ticker} Corp", 'Stock', 'USD')
    )
    conn.commit()

def load_price_data(ticker):
    csv_file = os.path.join("dataset", f"{ticker}_price_data.csv")
    if not os.path.exists(csv_file):
        print(f"⚠️ CSV not found for {ticker}")
        return

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip().str.lower()

    # Drop rows with missing 'date'
    df = df[df['date'].notna()]

    curr.execute("SELECT asset_id FROM assets WHERE ticker = %s", (ticker,))
    result = curr.fetchone()
    if not result:
        print(f"❌ {ticker} not found in assets table")
        return

    asset_id = result[0]

    for _, row in df.iterrows():
        try:
            curr.execute(
                """INSERT INTO price_data (asset_id, trade_date, high, low, close, volume, adjusted_close)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (asset_id, trade_date) DO NOTHING""",
                (
                    asset_id,
                    pd.to_datetime(row['date']).date(),
                    row['high'],
                    row['low'],
                    row['close'],
                    row['volume'],
                    row.get('adj close') or row.get('adjusted_close')
                )
            )
        except Exception as e:
            print(f"Error inserting row for {ticker} on {row['date']}: {e}")

    conn.commit()
    print(f"✅ {ticker} data loaded")


for ticker in tickers['ticker']:
    insert_asset(ticker)
    load_price_data(ticker)

curr.close()
conn.close()
