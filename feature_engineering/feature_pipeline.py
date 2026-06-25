from feature_engineering.indicators.trend import calculate_sma , calculate_ema, calculate_wma,calculate_hma
from database.queries import  get_stock_dataframe
from feature_engineering.features.trend_feature import create_trend_features



df = get_stock_dataframe("HDFCBANK.NS")

for window in [20, 50, 200]:
    df = calculate_sma(df, window)

for window in [20, 50, 200]:
    df = calculate_ema(df, window)

for window in [20, 50, 200]:
    df = calculate_wma(df, window)

for window in [20, 50, 200]:
    df = calculate_hma(df, window)

df = create_trend_features(df)


print(df.tail())
print("-"*50)
print(df.head())