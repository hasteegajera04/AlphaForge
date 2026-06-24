import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing Database Integration...")
print("=" * 60)

try:
    from validation.pipeline import validate_dataset
    from database.connection import init_database
    from database.storage import insert_validated_stock_data
    from database.db_query import load_stock_data_from_db
    from database import (
        stock_exists,
        get_stock_dataframe,
        get_all_symbols,
        get_latest_price,
        get_stock_metadata,
        get_latest_n_rows,
        get_price_between_dates,
        get_stocks_by_status,
        get_validation_result,
        get_download_log,
    )
    print("OK - All imports successful")
    print()
    
    # Check database schema
    init_database()
    print("OK - Database initialized")
    print()
    
    # List tables
    import sqlite3
    conn = sqlite3.connect('data/stocks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("OK - Database tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check record counts
    cursor.execute("SELECT COUNT(*) FROM stock_prices")
    price_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM validation_metadata")
    metadata_count = cursor.fetchone()[0]
    
    print()
    print(f"OK - Total price records: {price_count}")
    print(f"OK - Total metadata records: {metadata_count}")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("Integration test PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
