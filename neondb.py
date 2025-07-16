import subprocess
import os

# Set environment variable for password
os.environ["PGPASSWORD"] = "bablu365"  # ← Replace this

LOCAL_DB_NAME = "portfolio_management"  # ← Your DB name
LOCAL_DB_USER = "postgres"              # ← Your DB user
DUMP_FILE = "local_backup.sql"

PG_DUMP_PATH = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

subprocess.run([
    PG_DUMP_PATH,
    "-U", LOCAL_DB_USER,
    "-d", LOCAL_DB_NAME,
    "-f", DUMP_FILE
], check=True)

print("✅ Local DB exported to local_backup.sql")
