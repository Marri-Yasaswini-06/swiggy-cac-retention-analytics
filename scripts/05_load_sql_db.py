"""
Loads the cleaned CSVs into a real SQL database (SQLite) with a proper relational schema
(primary keys, a foreign key, an index) instead of leaving the analysis in flat CSVs/pandas.

Why SQLite and not PostgreSQL/MySQL: this is a portfolio project meant to run with zero setup
for anyone reviewing the repo -- SQLite is a real, production-grade SQL engine (not a toy),
it just doesn't need a separate server process. The schema and queries below are standard SQL
and would run unchanged against PostgreSQL/MySQL if this were plugged into a real warehouse.
"""
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN = BASE_DIR / "data/clean"
DB = BASE_DIR / "database/swiggy_analytics.db"
DB.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB))
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS interactions;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id        TEXT PRIMARY KEY,
    full_name          TEXT,
    email               TEXT,
    phone               TEXT,
    city                TEXT,
    signup_date         TEXT,
    segment             TEXT,
    swiggy_one_member   INTEGER,   -- 0/1 boolean
    marketing_opt_in    INTEGER    -- 0/1 boolean
);

CREATE TABLE interactions (
    interaction_id  TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL,
    campaign_name   TEXT,
    channel         TEXT,
    event_date      TEXT,
    sent            INTEGER,
    opened          INTEGER,
    clicked         INTEGER,
    converted       INTEGER,
    order_value     REAL,
    spend           REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_interactions_customer ON interactions(customer_id);
CREATE INDEX idx_interactions_channel  ON interactions(channel);
CREATE INDEX idx_interactions_campaign ON interactions(campaign_name);
""")

cust = pd.read_csv(f"{CLEAN}/crm_customers_clean.csv")
cust["swiggy_one_member"] = cust["swiggy_one_member"].astype(bool).astype(int)
cust["marketing_opt_in"] = cust["marketing_opt_in"].astype(bool).astype(int)
cust.to_sql("customers", conn, if_exists="append", index=False)

inter = pd.read_csv(f"{CLEAN}/marketing_interactions_clean.csv")
inter.to_sql("interactions", conn, if_exists="append", index=False)

conn.commit()

n_cust = cur.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
n_int = cur.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
n_orphan = cur.execute("""
    SELECT COUNT(*) FROM interactions i
    LEFT JOIN customers c ON i.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
""").fetchone()[0]

print(f"Loaded {n_cust} customers, {n_int} interactions into {DB}")
print(f"Referential integrity check: {n_orphan} orphaned interactions (should be 0)")

conn.close()
