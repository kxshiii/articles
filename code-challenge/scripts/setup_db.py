# Setup script to initialize the database with schema and seed data
import os
import sqlite3
from lib.db.connection import DB_PATH
from lib.db.seed import seed

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '../lib/db/schema.sql')

def setup_db():
    # Remove existing database to ensure a clean state
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    # Create database and tables
    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.executescript(schema_sql)
    finally:
        conn.close()
    # Seed data
    seed()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_db()
