import pandas as pd
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.database import init_database
from ingestion.storage import insert_validated_stock_data, get_validation_status


def migrate_csv_to_database():
    """
    Migrate existing validated CSV files from data/raw/ to database.
    This is a one-time backfill operation.
    """
    
    # Initialize database
    init_database()
    
    csv_directory = "data/raw"
    
    if not os.path.exists(csv_directory):
        print(f"Directory {csv_directory} not found")
        return
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv")]
    
    if not csv_files:
        print("No CSV files found in data/raw/")
        return
    
    print(f"Found {len(csv_files)} CSV files to migrate")
    print("-" * 50)
    
    for csv_file in csv_files:
        symbol = csv_file.replace(".csv", "")
        csv_path = os.path.join(csv_directory, csv_file)
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            
            # Check if data already exists in database
            existing = get_validation_status(symbol)
            if existing:
                print(f"✓ {symbol} - Already in database, skipping")
                continue
            
            # For migration, we use default score and status
            # In a real scenario, you might want to re-validate
            score = 100.0
            status = "EXCELLENT"
            
            # Insert data
            result = insert_validated_stock_data(symbol, df, score, status)
            
            if result["success"]:
                print(f"✓ {symbol} - Migrated {len(df)} rows")
            else:
                print(f"✗ {symbol} - Migration failed: {result['message']}")
        
        except Exception as error:
            print(f"✗ {symbol} - Error: {error}")
    
    print("-" * 50)
    print("Migration complete!")


if __name__ == "__main__":
    migrate_csv_to_database()
