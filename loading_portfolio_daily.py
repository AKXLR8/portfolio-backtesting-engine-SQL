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




# Connect to Neon DB
neon_conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_VfmpQuI3rWK1@ep-dark-forest-a16bt9bq-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
neon_cur = neon_conn.cursor()

# Upload metrics
for _, row in df_metrics.iterrows():
    neon_cur.execute("""
        INSERT INTO portfolio_metrics (portfolio_id, annual_return, annual_volatility, sharpe_ratio)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (portfolio_id) DO UPDATE SET
            annual_return = EXCLUDED.annual_return,
            annual_volatility = EXCLUDED.annual_volatility,
            sharpe_ratio = EXCLUDED.sharpe_ratio
    """, (
        int(row['portfolio_id']),
        float(row['annual_return']),
        float(row['annual_volatility']),
        float(row['sharpe_ratio'])
    ))

neon_conn.commit()
neon_cur.close()
neon_conn.close()
print("✅ Portfolio metrics uploaded to Neon DB")


