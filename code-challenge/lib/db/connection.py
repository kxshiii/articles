# SQLite database connection module
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../../articles.db')

def get_connection():
    """
    Returns a SQLite connection with row_factory set to sqlite3.Row for dict-like access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
