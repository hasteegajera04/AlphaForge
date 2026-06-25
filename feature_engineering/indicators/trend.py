import pandas as pd

def calculate_sma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    column_name = f"sma_{window}"

    df[column_name] = (df["close"].rolling(window=window, min_periods=window).mean())

    return df

def calculate_ema(df: pd.DataFrame, window: int) -> pd.DataFrame:
    column_name = f"ema_{window}"

    df[column_name] = df["close"].ewm(span=window, adjust=False).mean()

    return df

def calculate_wma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    column_name = f"wma_{window}"

    weights = list(range(1, window + 1))
    df[column_name] = df["close"].rolling(window=window).apply(lambda prices: (prices * weights).sum() / sum(weights), raw=True)

    return df

def calculate_hma(df:pd.DataFrame , window:int) -> pd.DataFrame :
    column_name = f"hma_{window}"
    half_length = int(window / 2)
    sqrt_length = int(window ** 0.5)

    wma_half =calculate_wma(df, half_length)
    wma_full = calculate_wma(df, window)

    raw_hma = 2 * wma_half[f"wma_{half_length}"] - wma_full[f"wma_{window}"]

    weights = list(range(1, sqrt_length + 1))

    df[column_name] = raw_hma.rolling(window=sqrt_length).apply(lambda x: (x * weights).sum() / sum(weights), raw=True)

    return df

