import sqlite3
from .connection import get_connection, close_connection


def insert_validated_stock_data(symbol, dataframe, score, status):
    """
    Insert validated stock data into the database.

    Args:
        symbol (str): Stock symbol (e.g., 'HDFCBANK.NS')
        dataframe (DataFrame): Pandas dataframe with OHLCV data
        score (float): Validation score (0-100)
        status (str): Validation status (EXCELLENT, GOOD, ACCEPTABLE, REJECT)

    Returns:
        dict: Result with success status and message
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()

        for date_index, row in dataframe.iterrows():
            date_str = str(date_index.date())

            cursor.execute('''
                INSERT OR REPLACE INTO stock_prices
                (symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                date_str,
                float(row['Open']) if 'Open' in row else None,
                float(row['High']) if 'High' in row else None,
                float(row['Low']) if 'Low' in row else None,
                float(row['Close']) if 'Close' in row else None,
                int(row['Volume']) if 'Volume' in row else 0
            ))

        cursor.execute('''
            INSERT OR REPLACE INTO validation_metadata
            (symbol, score, status, rows_count)
            VALUES (?, ?, ?, ?)
        ''', (symbol, score, status, len(dataframe)))

        connection.commit()
        close_connection(connection)

        return {
            "success": True,
            "message": f"Inserted {len(dataframe)} rows for {symbol}"
        }

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {
            "success": False,
            "message": f"Failed to insert data: {error}"
        }


def get_stock_data(symbol, start_date=None, end_date=None):
    """
    Retrieve stock data from the database.

    Args:
        symbol (str): Stock symbol
        start_date (str): Start date in format 'YYYY-MM-DD' (optional)
        end_date (str): End date in format 'YYYY-MM-DD' (optional)

    Returns:
        list: List of records
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM stock_prices WHERE symbol = ?"
        params = [symbol]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date ASC"

        cursor.execute(query, params)
        records = cursor.fetchall()
        close_connection(connection)

        return records

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return []


def get_all_symbols():
    """Get all unique stock symbols in the database."""

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol
        ''')

        symbols = [row[0] for row in cursor.fetchall()]
        close_connection(connection)

        return symbols

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return []


def get_validation_status(symbol):
    """Get validation metadata for a stock symbol."""

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT score, status, rows_count, last_updated
            FROM validation_metadata WHERE symbol = ?
        ''', (symbol,))

        record = cursor.fetchone()
        close_connection(connection)

        return record

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return None

