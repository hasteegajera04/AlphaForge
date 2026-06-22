import sqlite3
import os


DATABASE_PATH = "data/stocks.db"


def get_connection():
    """Get a SQLite database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    """Create database and tables if they don't exist."""
    connection = get_connection()
    cursor = connection.cursor()
    
    # Create stock_prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, date)
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_symbol_date 
        ON stock_prices(symbol, date)
    ''')
    
    # Create validation_metadata table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            score REAL,
            status TEXT,
            rows_count INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    connection.commit()
    connection.close()
    
    print(f"Database initialized at {DATABASE_PATH}")


def close_connection(connection):
    """Close database connection."""
    connection.close()
