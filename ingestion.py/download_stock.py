import yfinance as yf
import pandas as pd
from prettytable import PrettyTable

# Stock symbol
symbol = "RELIANCE.NS"

# Download data
df = yf.download(
    symbol,
    start="2020-01-01",
    end="2025-01-01",
    interval="1d"
)

# Create PrettyTable
table = PrettyTable()

# Add column names
table.field_names = df.columns.tolist()

# Add first 5 rows
for row in df.head().values:
    table.add_row(row)

# Print nice table
print("\nFirst 5 Rows of Stock Data:\n")
print(table)

# DataFrame information
print("\nData Information:\n")
df.info()

# Shape
print("\nDataset Shape:")
print(df.shape)

# Save CSV
output_path = f"data/raw/{symbol}.csv"

df.to_csv(output_path)

print(f"\nData saved to: {output_path}")