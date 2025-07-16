import psycopg2

NEON_CONN = "postgresql://neondb_owner:npg_VfmpQuI3rWK1@ep-dark-forest-a16bt9bq-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(NEON_CONN)
cur = conn.cursor()

with open("local_backup.sql", "r") as f:
    sql = f.read()
    cur.copy_expert(sql, f)

conn.commit()
cur.close()
conn.close()
print("✅ Loaded COPY data into Neon DB")


