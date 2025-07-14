import pandas as pd
import psycopg2

# Load the updated CSV
df = pd.read_csv("new_portfolio_daily_value.csv", parse_dates=['trade_date'])

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)
cur = conn.cursor()

# Insert data into the table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO portfolio_daily_value (portfolio_id, trade_date, portfolio_value)
        VALUES (%s, %s, %s)
    """, (int(row['portfolio_id']), row['trade_date'], float(row['portfolio_value'])))

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("✅ Inserted new_portfolio_daily_value.csv into PostgreSQL")
