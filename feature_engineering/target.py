
import pandas as pd


def generate_targets(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["future_return_5d"] = (
        df["close"].shift(-5) / df["close"]
    ) - 1

    return df
