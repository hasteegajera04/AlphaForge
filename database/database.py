import os
import sqlite3


DB_PATH = "data/algo_trading.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    os.makedirs("data", exist_ok=True)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            symbol TEXT PRIMARY KEY,
            start_date TEXT,
            end_date TEXT,
            rows INTEGER,
            last_updated TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS download_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            rows INTEGER,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            valid INTEGER,
            score REAL,
            status TEXT,
            errors TEXT,
            report_path TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_stock(symbol):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO stocks (symbol)
        VALUES (?)
    """, (symbol,))

    connection.commit()
    connection.close()


def save_stock_prices(symbol, df):
    connection = get_connection()
    cursor = connection.cursor()

    for date, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO stock_prices
            (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            symbol,
            str(date.date()),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            int(row["Volume"])
        ))

    connection.commit()
    connection.close()


def save_metadata(symbol, start_date, end_date, rows, last_updated):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO metadata
        (symbol, start_date, end_date, rows, last_updated)
        VALUES (?, ?, ?, ?, ?)
    """, (
        symbol,
        str(start_date),
        str(end_date),
        rows,
        last_updated
    ))

    connection.commit()
    connection.close()


def save_download_log(symbol, timestamp, rows, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO download_logs
        (symbol, timestamp, rows, status)
        VALUES (?, ?, ?, ?)
    """, (
        symbol,
        timestamp,
        rows,
        status
    ))

    connection.commit()
    connection.close()


def save_validation_result(symbol, timestamp, validation_result):
    connection = get_connection()
    cursor = connection.cursor()

    errors = "; ".join(validation_result["errors"])

    cursor.execute("""
        INSERT INTO validation_results
        (symbol, timestamp, valid, score, status, errors, report_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        symbol,
        timestamp,
        int(validation_result["valid"]),
        validation_result["score"],
        validation_result["status"],
        errors,
        validation_result["report"]
    ))

    connection.commit()
    connection.close()
