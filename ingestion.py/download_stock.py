import yfinance as yf
import pandas as pd
from symbol_loader import load_symbols

symbols = load_symbols()

for stock in symbols:

    df = yf.download(
        stock,
        start="2020-01-01",
        end="2025-01-01",
        interval="1d"
    )

    print(f"\nFirst 5 Rows for {stock}:\n")
    print(df.head())

    print(f"\nData Information for {stock}:\n")
    df.info()

    print(f"\nDataset Shape for {stock}:")
    print(df.shape)

    output_path = f"data/raw/{stock}.csv"

    df.to_csv(
        output_path,
        
    )

    print(f"\nData saved to: {output_path}")
