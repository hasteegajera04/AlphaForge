import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing Database Integration...")
print("=" * 60)

try:
    from validation.pipeline import validate_dataset
    from ingestion.database import init_database
    from ingestion.storage import insert_validated_stock_data
    from ingestion.db_query import load_stock_data_from_db
    print("✓ All imports successful")
    print()
    
    # Check database schema
    init_database()
    print("✓ Database initialized")
    print()
    
    # List tables
    import sqlite3
    conn = sqlite3.connect('data/stocks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("✓ Database tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check record counts
    cursor.execute("SELECT COUNT(*) FROM stock_prices")
    price_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM validation_metadata")
    metadata_count = cursor.fetchone()[0]
    
    print()
    print(f"✓ Total price records: {price_count}")
    print(f"✓ Total metadata records: {metadata_count}")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("Integration test PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
