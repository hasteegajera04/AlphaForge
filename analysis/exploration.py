import pandas as pd
import json

with open("config/stocks.json", "r") as file:
    data = json.load(file)

stocks = data["stocks"]

for stock in stocks:

    print("\n" + "=" * 60)
    print("STOCK:", stock)
    print("=" * 60)

    df = pd.read_csv(f"data/raw/{stock}.csv")

    print(df["Volume"].dtype)
    print(df["Volume"].head())
    

    print("\nRows:", df.shape[0])
    print("Columns:", df.shape[1])

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(df["Date"])

        print("\nOldest Record:")
        print(df["Date"].min())

        print("\nNewest Record:")
        print(df["Date"].max())

    print("\nMissing Values:")
    print(df.isnull().sum())

    if "Volume" in df.columns:

        print("\nAverage Daily Volume:")
        print(df["Volume"].mean())

    print("\nDataset Info:")
    df.info()

    print("\nSummary Statistics:")
    print(df.describe())

    