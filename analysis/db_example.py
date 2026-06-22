# Example: Using Database for Stock Analysis
# This shows how to read validated stock data from database instead of CSV files

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.db_query import (
    load_stock_data_from_db,
    get_all_available_stocks,
    get_stock_info,
    load_multiple_stocks
)


def example_load_single_stock():
    """Example 1: Load a single stock's data from database"""
    print("=" * 60)
    print("Example 1: Load Single Stock Data")
    print("=" * 60)
    
    # Load HDFCBANK.NS data
    df = load_stock_data_from_db('HDFCBANK.NS')
    
    print(f"Shape: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print("\nFirst 3 rows:")
    print(df.head(3))
    print("\nLast 3 rows:")
    print(df.tail(3))
    print()


def example_load_with_date_range():
    """Example 2: Load data with specific date range"""
    print("=" * 60)
    print("Example 2: Load Data with Date Range")
    print("=" * 60)
    
    # Load data for specific date range
    df = load_stock_data_from_db(
        'INFY.NS',
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    print(f"INFY.NS data for 2024: {len(df)} rows")
    print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
    print(f"\nAverage Close Price: {df['close'].mean():.2f}")
    print(f"Max Close Price: {df['close'].max():.2f}")
    print(f"Min Close Price: {df['close'].min():.2f}")
    print()


def example_multiple_stocks():
    """Example 3: Load multiple stocks and compare"""
    print("=" * 60)
    print("Example 3: Load Multiple Stocks")
    print("=" * 60)
    
    # Load multiple stocks
    symbols = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']
    df = load_multiple_stocks(symbols, start_date='2024-01-01')
    
    print(f"Combined data for {symbols}")
    print(f"Shape: {df.shape}")
    print("\nData by symbol:")
    for symbol in symbols:
        count = len(df.xs(symbol, level='symbol'))
        print(f"  {symbol}: {count} rows")
    print()


def example_get_stock_info():
    """Example 4: Get validation metadata for stocks"""
    print("=" * 60)
    print("Example 4: Get Stock Validation Info")
    print("=" * 60)
    
    # Get all available stocks
    symbols = get_all_available_stocks()
    print(f"All available stocks: {symbols}\n")
    
    # Get info for each stock
    for symbol in symbols:
        info = get_stock_info(symbol)
        if info:
            print(f"{symbol}:")
            print(f"  Score: {info['score']}")
            print(f"  Status: {info['status']}")
            print(f"  Rows: {info['rows_count']}")
            print(f"  Last Updated: {info['last_updated']}")
    print()


def example_simple_analysis():
    """Example 5: Simple technical analysis using database data"""
    print("=" * 60)
    print("Example 5: Simple Analysis")
    print("=" * 60)
    
    # Load data
    df = load_stock_data_from_db('HDFCBANK.NS', start_date='2024-01-01')
    
    # Calculate 50-day moving average
    df['MA50'] = df['close'].rolling(window=50).mean()
    
    # Calculate price change percentage
    df['Price_Change_Pct'] = df['close'].pct_change() * 100
    
    print("HDFCBANK.NS - 2024 Analysis:")
    print(f"Latest Close: {df['close'].iloc[-1]:.2f}")
    print(f"50-Day MA: {df['MA50'].iloc[-1]:.2f}")
    print(f"Avg Daily Change: {df['Price_Change_Pct'].mean():.2f}%")
    print("\nRecent data with MA and change:")
    print(df[['close', 'MA50', 'Price_Change_Pct']].tail(5))
    print()


if __name__ == "__main__":
    # Run all examples
    example_load_single_stock()
    example_load_with_date_range()
    example_multiple_stocks()
    example_get_stock_info()
    example_simple_analysis()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
