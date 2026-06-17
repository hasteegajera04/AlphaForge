import csv
from datetime import datetime

import yfinance as yf

from config.db_config import DATA_DIR, LOG_DIR, RAW_DATA_DIR
from database.database import (
    init_db,
    save_download_log,
    save_metadata,
    save_stock,
    save_stock_prices,
    save_validation_result,
)
from ingestion.symbol_loader import load_symbols
from validation.validator import validate_dataset


START_DATE = "2020-01-01"
END_DATE = "2025-01-01"
METADATA_CSV = DATA_DIR / "metadata.csv"
DOWNLOAD_LOG_CSV = LOG_DIR / "download_log.csv"


def _ensure_runtime_directories():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _write_csv_header(path, header):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)


def _append_csv_row(path, row):
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)


def main():
    _ensure_runtime_directories()
    init_db()

    stocks = load_symbols()

    _write_csv_header(
        METADATA_CSV,
        ["symbol", "start_date", "end_date", "rows", "last_updated"],
    )
    _write_csv_header(
        DOWNLOAD_LOG_CSV,
        ["symbol", "timestamp", "rows", "status"],
    )

    for stock in stocks:
        save_stock(stock)

        ticker = yf.Ticker(stock)
        df = ticker.history(start=START_DATE, end=END_DATE)
        validation_result = validate_dataset(stock, df)

        rows = len(df)
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")

        if validation_result["valid"]:
            status = "SUCCESS"
            df.to_csv(RAW_DATA_DIR / f"{stock}.csv")

            start_date = df.index.min().date()
            end_date = df.index.max().date()

            _append_csv_row(
                METADATA_CSV,
                [stock, start_date, end_date, rows, timestamp],
            )

            save_stock_prices(stock, df)
            save_metadata(stock, start_date, end_date, rows, timestamp)

            print(f"{stock} passed validation")
        else:
            status = "FAILED"
            print(f"{stock} failed validation")
            print(validation_result["errors"])

        _append_csv_row(
            DOWNLOAD_LOG_CSV,
            [stock, timestamp, rows, status],
        )

        save_download_log(stock, timestamp, rows, status)
        save_validation_result(stock, timestamp, validation_result)

        print(f"Score: {validation_result['score']}")
        print(f"Status: {validation_result['status']}")
        print(f"Report: {validation_result['report']}")
        print("--" * 30)


if __name__ == "__main__":
    main()
