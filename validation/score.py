# 1. COMPLETENESS
def completeness_score(df):
    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_cells = df.isnull().sum().sum()

    return 1 - (missing_cells / total_cells)


# 2. INTEGRITY (OHLC logic)
def integrity_score(df):
    required = ["Open", "High", "Low", "Close"]

    for column in required:
        if column not in df.columns:
            return 0

    invalid = 0
    total = len(df)

    if total == 0:
        return 0

    for _, row in df.iterrows():

        if (
            row["High"] < max(row["Open"], row["Close"]) or
            row["Low"] > min(row["Open"], row["Close"])
        ):
            invalid += 1

    return 1 - (invalid / total if total > 0 else 1)


# 3. CONSISTENCY (duplicates + ordering)
def consistency_score(df):
    if len(df) == 0:
        return 0

    duplicate_penalty = df.index.duplicated().sum() / len(df)

    ordering_penalty = 0 if df.index.is_monotonic_increasing else 1

    return 1 - min(1, duplicate_penalty + ordering_penalty)


# 4. VALIDITY (volume + negative values)
def validity_score(df):
    required = ["Open", "High", "Low", "Close", "Volume"]

    for column in required:
        if column not in df.columns:
            return 0

    if len(df) == 0:
        return 0

    invalid_volume = (df["Volume"] < 0).sum() / len(df)

    invalid_prices = (
        (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1).sum()
        / len(df)
    )

    return 1 - min(1, invalid_volume + invalid_prices)


# 5. FINAL SCORE (weighted model)
def calculate_professional_score(df):

    c1 = completeness_score(df)
    c2 = integrity_score(df)
    c3 = consistency_score(df)
    c4 = validity_score(df)

    weights = {
        "completeness": 0.30,
        "integrity": 0.30,
        "consistency": 0.20,
        "validity": 0.20
    }

    final_score = (
        c1 * weights["completeness"] +
        c2 * weights["integrity"] +
        c3 * weights["consistency"] +
        c4 * weights["validity"]
    )

    return float(round(final_score * 100, 2))


# 6. DECISION ENGINE (PRO LEVEL)
def classify_dataset(score):

    if score >= 95:
        return "EXCELLENT"
    elif score >= 85:
        return "GOOD"
    elif score >= 70:
        return "ACCEPTABLE"
    else:
        return "REJECT"


def calculate_score(df, errors=None):
    if errors is None:
        errors = []

    if "Empty DataFrame" in errors:
        return 0

    if "Missing Required Columns" in errors:
        return 0

    return calculate_professional_score(df)


def get_status(score):
    return classify_dataset(score)
