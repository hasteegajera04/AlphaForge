def check_empty(df):
    return not df.empty


def check_required_columns(df):
    required = ["Open", "High", "Low", "Close", "Volume"]

    for column in required:
        if column not in df.columns:
            return False

    return True


def check_missing_values(df):
    return not df.isnull().values.any()


def check_duplicate_rows(df):
    return not df.index.duplicated().any()


def check_price_logic(df):
    for _, row in df.iterrows():

        if row["High"] < row["Open"]:
            return False

        if row["High"] < row["Close"]:
            return False

        if row["Low"] > row["Open"]:
            return False

        if row["Low"] > row["Close"]:
            return False

    return True


def check_volume(df):
    return (df["Volume"] >= 0).all()