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

print(get_all_symbols())
print("-"*50)
print("stock_exists('HDFCBANK.NS'):", stock_exists("HDFCBANK.NS"))
print("-"*50)
print("get_stock_dataframe('HDFCBANK.NS'):", get_stock_dataframe("HDFCBANK.NS"))
print("-"*50)
print("get_latest_price('HDFCBANK.NS'):", get_latest_price("HDFCBANK.NS"))
print("-"*50)
print("get_stock_metadata('HDFCBANK.NS'):", get_stock_metadata("HDFCBANK.NS"))
print("-"*50)
print("get_latest_n_rows('HDFCBANK.NS', 5):", get_latest_n_rows("HDFCBANK.NS", 5))
print("-"*50)
print("get_price_between_dates('HDFCBANK.NS', '2023-01-01', '2023-12-31'):", get_price_between_dates("HDFCBANK.NS", "2023-01-01", "2023-12-31"))
print("-"*50)
print("get_stocks_by_status('validated'):", get_stocks_by_status("EXCELLENT"))
print("-"*50)
print("get_validation_result('HDFCBANK.NS'):", get_validation_result("HDFCBANK.NS"))
print("-"*50)
print("get_download_log('HDFCBANK.NS'):", get_download_log("HDFCBANK.NS"))
print("-"*50)