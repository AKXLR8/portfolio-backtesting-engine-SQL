import pandas as pd
import psycopg2

# Load the CSV
df = pd.read_csv("portfolio_daily_value.csv", parse_dates=['trade_date'])

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)
cur = conn.cursor()

# Insert data row by row
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO portfolio_daily_value (portfolio_id, trade_date, portfolio_value)
        VALUES (%s, %s, %s)
    """, (row['portfolio_id'], row['trade_date'], row['portfolio_value']))

conn.commit()
cur.close()
conn.close()

print("✅ portfolio_daily_value loaded into DB.")
