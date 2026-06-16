import yfinance as yf
import csv
import os
from datetime import datetime
from .symbol_loader import load_symbols
from validation.pipeline import validate_dataset


def main():
   
    stocks = load_symbols()

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
            end="2025-01-01"
        )

        validation_result = validate_dataset(stock, df)
        rows = len(df)
        time = datetime.now().strftime("%d-%m-%y %H:%M:%S")

        if validation_result["valid"]:
            status = "SUCCESS"
            df.to_csv(f"data/raw/{stock}.csv")
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

            print(f"{stock} passed validation")
        else:
            status = "FAILED"
            print(f"{stock} failed validation")
            print(validation_result["errors"])

        with open("logs/download_log.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                stock,
                time,
                rows,
                status
            ])

        print(f"Score: {validation_result['score']}")
        print(f"Status: {validation_result['status']}")
        print(f"Report: {validation_result['report']}")
        print("--" * 30)


if __name__ == "__main__":
    main()
