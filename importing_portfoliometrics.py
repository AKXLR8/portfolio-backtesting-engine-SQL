import pandas as pd
import psycopg2

# Local PostgreSQL
local_conn = psycopg2.connect(
    host="localhost",
    dbname="portfolio_management",
    user="postgres",
    password="bablu365"
)
local_cur = local_conn.cursor()

# Fetch metrics
query = """
SELECT
    portfolio_id,
    ROUND(AVG(daily_return) * 252::numeric, 2),
    ROUND((STDDEV(daily_return) * SQRT(252))::numeric, 2),
    ROUND((AVG(daily_return) * 252) / (STDDEV(daily_return) * SQRT(252))::numeric, 2)
FROM daily_returns GROUP BY portfolio_id;
"""

df_metrics = pd.read_sql(query, local_conn)

local_cur.close()
local_conn.close()
