import pandas as pd
from .storage import get_stock_data, get_all_symbols, get_validation_status


def load_stock_data_from_db(symbol, start_date=None, end_date=None):
    """
    Load stock data from database as a pandas DataFrame.

    Args:
        symbol (str): Stock symbol (e.g., 'HDFCBANK.NS')
        start_date (str): Start date in format 'YYYY-MM-DD' (optional)
        end_date (str): End date in format 'YYYY-MM-DD' (optional)

    Returns:
        DataFrame: Stock data with columns: symbol, date, open, high, low, close, volume
    """

    records = get_stock_data(symbol, start_date, end_date)

    if not records:
        print(f"No data found for {symbol}")
        return pd.DataFrame()

    data = []
    for record in records:
        data.append({
            'symbol': record[1],
            'date': record[2],
            'open': record[3],
            'high': record[4],
            'low': record[5],
            'close': record[6],
            'volume': record[7]
        })

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    return df


def get_all_available_stocks():
    """Get all unique stock symbols available in the database."""
    symbols = get_all_symbols()
    return symbols


def get_stock_info(symbol):
    """
    Get validation information for a stock symbol.

    Returns:
        dict: Contains score, status, rows_count, last_updated
    """

    record = get_validation_status(symbol)

    if not record:
        return None

    return {
        'symbol': symbol,
        'score': record[0],
        'status': record[1],
        'rows_count': record[2],
        'last_updated': record[3]
    }


def load_multiple_stocks(symbols, start_date=None, end_date=None):
    """
    Load multiple stocks data and combine into single DataFrame.

    Args:
        symbols (list): List of stock symbols
        start_date (str): Start date in format 'YYYY-MM-DD' (optional)
        end_date (str): End date in format 'YYYY-MM-DD' (optional)

    Returns:
        DataFrame: Combined data with multi-index (symbol, date)
    """

    all_data = []

    for symbol in symbols:
        df = load_stock_data_from_db(symbol, start_date, end_date)
        if not df.empty:
            df['symbol'] = symbol
            all_data.append(df)

    if not all_data:
        print("No data found for any symbol")
        return pd.DataFrame()

    combined_df = pd.concat(all_data)
    combined_df = combined_df.set_index('symbol', append=True)

    return combined_df

