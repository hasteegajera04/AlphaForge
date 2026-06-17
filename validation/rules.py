REQUIRED_PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


def check_empty(df):
    return not df.empty


def check_required_columns(df):
    return all(column in df.columns for column in REQUIRED_PRICE_COLUMNS)


def check_missing_values(df):
    return not df.isnull().values.any()


def check_duplicate_rows(df):
    return not df.index.duplicated().any()


def check_price_logic(df):
    required = ("Open", "High", "Low", "Close")
    if not all(column in df.columns for column in required):
        return False

    highest_prices = df[["Open", "Close"]].max(axis=1)
    lowest_prices = df[["Open", "Close"]].min(axis=1)

    return (
        (df["High"] >= highest_prices)
        & (df["Low"] <= lowest_prices)
    ).all()


def check_volume(df):
    if "Volume" not in df.columns:
        return False

    return (df["Volume"] >= 0).all()
