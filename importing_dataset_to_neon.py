import psycopg2

NEON_CONN = "postgre"

conn = psycopg2.connect(NEON_CONN)
cur = conn.cursor()

with open("local_backup.sql", "r") as f:
    sql = f.read()
    cur.copy_expert(sql, f)

conn.commit()
cur.close()
conn.close()
print("✅ Loaded COPY data into Neon DB")


