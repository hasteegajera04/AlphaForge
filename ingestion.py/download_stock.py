import yfinance as yf
import json
import csv
from datetime import datetime
from symbol_loader import load_symbols

data = load_symbols()
stocks = data

with open("data/metadata.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "symbol",
        "start_date",
        "end_date",
        "rows",
        "last_updated"
    ])

with open("logs/download_log.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "symbol",
        "timestamp",
        "rows",
        "status"
    ])

for stock in stocks:

    ticker = yf.Ticker(stock)
    df = ticker.history(
        start="2020-01-01",
        end="2025-01-01") 
        
    
    df = df.drop(
    columns=["Dividends", "Stock Splits"])

    rows = len(df)

    if rows > 0:
        status = "SUCCESS"
    else:
        status = "FAILED"

    df.to_csv(f"data/raw/{stock}.csv")

    time = datetime.now().strftime("%d-%m-%y %H:%M:%S")

    start_date = df.index.min().date()
    end_date = df.index.max().date()

    with open("data/metadata.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            stock,
            start_date,
            end_date,
            rows,
            time
            ])   
        
    with open("logs/download_log.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            stock,
            time,
            rows,
            status
        ])

    print(stock, status)
   
 


