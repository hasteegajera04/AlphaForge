from database.database import get_connection


def fetch_all(symbol):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
    """, (symbol,))

    data = cursor.fetchall()
    connection.close()

    return data


def count_rows(table_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total = cursor.fetchone()[0]

    connection.close()

    return total
