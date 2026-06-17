from contextlib import contextmanager

import pandas as pd
import sqlite3

from config.db_config import DB_PATH, DB_TYPE, DATA_DIR


ALLOWED_TABLES = {
    "stocks",
    "stock_prices",
    "metadata",
    "download_logs",
    "validation_results",
}


def get_connection():
    if DB_TYPE != "sqlite":
        raise NotImplementedError("Postgres support is not implemented yet")

    return sqlite3.connect(str(DB_PATH))


@contextmanager
def db_connection():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


def _validate_table_name(table_name):
    if table_name not in ALLOWED_TABLES:
        allowed = ", ".join(sorted(ALLOWED_TABLES))
        raise ValueError(f"Unsupported table '{table_name}'. Allowed tables: {allowed}")


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    schema = """
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS stock_prices (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        );

        CREATE TABLE IF NOT EXISTS metadata (
            symbol TEXT PRIMARY KEY,
            start_date TEXT,
            end_date TEXT,
            rows INTEGER,
            last_updated TEXT
        );

        CREATE TABLE IF NOT EXISTS download_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            rows INTEGER,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            valid INTEGER,
            score REAL,
            status TEXT,
            errors TEXT,
            report_path TEXT
        );
    """

    with db_connection() as connection:
        connection.executescript(schema)
        connection.commit()


def save_stock(symbol):
    with db_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO stocks (symbol)
            VALUES (?)
            """,
            (symbol,),
        )
        connection.commit()


def save_stock_prices(symbol, df):
    if df.empty:
        return 0

    records = [
        (
            symbol,
            pd.Timestamp(index).date().isoformat(),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            int(row["Volume"]),
        )
        for index, row in df.iterrows()
    ]

    with db_connection() as connection:
        connection.executemany(
            """
            INSERT OR REPLACE INTO stock_prices
            (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            records,
        )
        connection.commit()

    return len(records)


def save_metadata(symbol, start_date, end_date, rows, last_updated):
    with db_connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO metadata
            (symbol, start_date, end_date, rows, last_updated)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                symbol,
                str(start_date),
                str(end_date),
                rows,
                last_updated,
            ),
        )
        connection.commit()


def save_download_log(symbol, timestamp, rows, status):
    with db_connection() as connection:
        connection.execute(
            """
            INSERT INTO download_logs
            (symbol, timestamp, rows, status)
            VALUES (?, ?, ?, ?)
            """,
            (symbol, timestamp, rows, status),
        )
        connection.commit()


def save_validation_result(symbol, timestamp, validation_result):
    errors = "; ".join(validation_result["errors"])

    with db_connection() as connection:
        connection.execute(
            """
            INSERT INTO validation_results
            (symbol, timestamp, valid, score, status, errors, report_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                timestamp,
                int(validation_result["valid"]),
                validation_result["score"],
                validation_result["status"],
                errors,
                validation_result["report"],
            ),
        )
        connection.commit()


def fetch_stock_prices(symbol):
    with db_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                symbol,
                date,
                open,
                high,
                low,
                close,
                volume
            FROM stock_prices
            WHERE symbol = ?
            ORDER BY date
            """,
            (symbol,),
        )
        return cursor.fetchall()


def load_table(table_name):
    _validate_table_name(table_name)

    with db_connection() as connection:
        return pd.read_sql(f"SELECT * FROM {table_name}", connection)


def count_rows(table_name):
    _validate_table_name(table_name)

    with db_connection() as connection:
        cursor = connection.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
