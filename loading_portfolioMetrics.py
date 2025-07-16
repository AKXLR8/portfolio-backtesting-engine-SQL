import pandas as pd
import psycopg2

# Step 1: Connect to your local PostgreSQL (source of truth)
local_conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)
local_cursor = local_conn.cursor()

# Step 2: Read portfolio metrics from local DB
query = """
SELECT
    portfolio_id,
    ROUND(AVG(daily_return) * 252::numeric, 2) AS annual_return,
    ROUND(STDDEV(daily_return) * SQRT(252)::numeric, 2) AS annual_volatility,
    ROUND((AVG(daily_return) * 252) / (STDDEV(daily_return) * SQRT(252))::numeric, 2) AS sharpe_ratio
FROM daily_returns
GROUP BY portfolio_id;
"""

df_metrics = pd.read_sql(query, local_conn)

# Close local connection
local_cursor.close()
local_conn.close()

# Step 3: Connect to Neon PostgreSQL
neon_conn = psycopg2.connect(
    "postgresql://neondb_owner:npg_VfmpQuI3rWK1@ep-dark-forest-a16bt9bq-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)
neon_cur = neon_conn.cursor()

# Step 4: Upload to Neon
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
