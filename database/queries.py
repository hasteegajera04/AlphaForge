import sqlite3
import pandas as pd
from .connection import get_connection, close_connection


def stock_exists(symbol):
    """Check if a stock exists in the database."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 FROM stock_prices WHERE symbol = ? LIMIT 1",
            (symbol,)
        )

        record = cursor.fetchone()
        close_connection(connection)

        return record is not None

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return False


def get_stock_dataframe(symbol):
    """Get complete OHLCV history for one stock as a pandas DataFrame."""
    try:
        connection = get_connection()

        query = '''
            SELECT date, open, high, low, close, volume
            FROM stock_prices
            WHERE symbol = ?
            ORDER BY date ASC
        '''

        df = pd.read_sql_query(query, connection, params=(symbol,))
        close_connection(connection)

        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")

        return df

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return pd.DataFrame()


def get_latest_n_rows(symbol, n):
    """Return the last N trading days for one stock as a DataFrame."""
    try:
        connection = get_connection()

        query = '''
            SELECT date, open, high, low, close, volume
            FROM stock_prices
            WHERE symbol = ?
            ORDER BY date DESC
            LIMIT ?
        '''

        df = pd.read_sql_query(query, connection, params=(symbol, n))
        close_connection(connection)

        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df = df.set_index("date")

        return df

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return pd.DataFrame()


def get_price_between_dates(symbol, start_date, end_date):
    """Return stock price data between two dates as a DataFrame."""
    try:
        connection = get_connection()

        query = '''
            SELECT date, open, high, low, close, volume
            FROM stock_prices
            WHERE symbol = ?
            AND date >= ?
            AND date <= ?
            ORDER BY date ASC
        '''

        df = pd.read_sql_query(
            query,
            connection,
            params=(symbol, start_date, end_date)
        )
        close_connection(connection)

        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")

        return df

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return pd.DataFrame()


def get_all_symbols():
    """Return a list of all stored stock symbols."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol")
        symbols = [row["symbol"] for row in cursor.fetchall()]
        close_connection(connection)

        return symbols

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return []


def get_stocks_by_status(status):
    """Return all stock symbols with a specific validation status."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT symbol
            FROM validation_metadata
            WHERE LOWER(status) = LOWER(?)
            ORDER BY symbol
        ''', (status,))

        symbols = [row["symbol"] for row in cursor.fetchall()]
        close_connection(connection)

        return symbols

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return []


def get_latest_price(symbol):
    """Return the latest available trading day's OHLCV data."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT symbol, date, open, high, low, close, volume
            FROM stock_prices
            WHERE symbol = ?
            ORDER BY date DESC
            LIMIT 1
        ''', (symbol,))

        record = cursor.fetchone()
        close_connection(connection)

        if record is None:
            return {}

        return dict(record)

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {}


def get_validation_result(symbol):
    """Return validation status and score for one stock."""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT symbol, score, status, rows_count, last_updated
            FROM validation_metadata
            WHERE symbol = ?
        ''', (symbol,))

        record = cursor.fetchone()
        close_connection(connection)

        if record is None:
            return {}

        return dict(record)

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {}


def get_download_log(symbol):
    """Return download history and timestamps for one stock."""
    try:
        log_path = "logs/download_log.csv"
        df = pd.read_csv(log_path)
        df = df[df["symbol"] == symbol]

        if df.empty:
            return {}

        records = df.to_dict("records")

        return {
            "symbol": symbol,
            "downloads": records,
            "latest_download": records[-1]
        }

    except FileNotFoundError:
        print("Download log file not found")
        return {}
    except KeyError as error:
        print(f"Download log column missing: {error}")
        return {}


def get_stock_metadata(symbol):
    """
    Return database metadata for one stock.

    company_name and sector are None because they are not stored yet.
    exchange is guessed from the symbol suffix.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT
                MIN(date) AS start_date,
                MAX(date) AS end_date,
                COUNT(*) AS price_rows
            FROM stock_prices
            WHERE symbol = ?
        ''', (symbol,))
        price_info = cursor.fetchone()

        cursor.execute('''
            SELECT score, status, rows_count, last_updated
            FROM validation_metadata
            WHERE symbol = ?
        ''', (symbol,))
        validation_info = cursor.fetchone()

        close_connection(connection)

        if price_info["price_rows"] == 0:
            return {}

        exchange = None
        if symbol.endswith(".NS"):
            exchange = "NSE"
        elif symbol.endswith(".BO"):
            exchange = "BSE"

        metadata = {
            "symbol": symbol,
            "company_name": None,
            "sector": None,
            "exchange": exchange,
            "start_date": price_info["start_date"],
            "end_date": price_info["end_date"],
            "price_rows": price_info["price_rows"],
            "validation_score": None,
            "validation_status": None,
            "validation_rows": None,
            "last_updated": None
        }

        if validation_info:
            metadata["validation_score"] = validation_info["score"]
            metadata["validation_status"] = validation_info["status"]
            metadata["validation_rows"] = validation_info["rows_count"]
            metadata["last_updated"] = validation_info["last_updated"]

        return metadata

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {}
