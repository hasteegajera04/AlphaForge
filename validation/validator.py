from validation.report import generate_report
from validation.rules import (
    check_duplicate_rows,
    check_empty,
    check_missing_values,
    check_price_logic,
    check_required_columns,
    check_volume,
)


SCORE_WEIGHTS = {
    "completeness": 0.30,
    "integrity": 0.30,
    "consistency": 0.20,
    "validity": 0.20,
}

STATUS_BANDS = (
    (95, "EXCELLENT"),
    (85, "GOOD"),
    (70, "ACCEPTABLE"),
)


def _completeness_score(df):
    total_cells = df.shape[0] * df.shape[1]
    if total_cells == 0:
        return 0.0

    missing_cells = df.isnull().sum().sum()
    return 1 - (missing_cells / total_cells)


def _integrity_score(df):
    required = ("Open", "High", "Low", "Close")
    if not all(column in df.columns for column in required):
        return 0.0

    if df.empty:
        return 0.0

    invalid_rows = (
        (df["High"] < df[["Open", "Close"]].max(axis=1))
        | (df["Low"] > df[["Open", "Close"]].min(axis=1))
    ).sum()

    return 1 - (invalid_rows / len(df))


def _consistency_score(df):
    if df.empty:
        return 0.0

    duplicate_penalty = df.index.duplicated().sum() / len(df)
    ordering_penalty = 0 if df.index.is_monotonic_increasing else 1

    return 1 - min(1, duplicate_penalty + ordering_penalty)


def _validity_score(df):
    required = ("Open", "High", "Low", "Close", "Volume")
    if not all(column in df.columns for column in required):
        return 0.0

    if df.empty:
        return 0.0

    invalid_volume = (df["Volume"] < 0).sum() / len(df)
    invalid_prices = (
        (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1).sum() / len(df)
    )

    return 1 - min(1, invalid_volume + invalid_prices)


def calculate_professional_score(df):
    score = (
        _completeness_score(df) * SCORE_WEIGHTS["completeness"]
        + _integrity_score(df) * SCORE_WEIGHTS["integrity"]
        + _consistency_score(df) * SCORE_WEIGHTS["consistency"]
        + _validity_score(df) * SCORE_WEIGHTS["validity"]
    )
    return float(round(score * 100, 2))


def classify_dataset(score):
    for threshold, label in STATUS_BANDS:
        if score >= threshold:
            return label

    return "REJECT"


def calculate_score(df, errors=None):
    errors = errors or []

    if "Empty DataFrame" in errors:
        return 0.0

    if "Missing Required Columns" in errors:
        return 0.0

    return calculate_professional_score(df)


def get_status(score):
    return classify_dataset(score)


def validate(df):
    errors = []

    has_required_columns = check_required_columns(df)

    if not check_empty(df):
        errors.append("Empty DataFrame")

    if not has_required_columns:
        errors.append("Missing Required Columns")
    else:
        if not check_missing_values(df):
            errors.append("Missing Values Found")

        if not check_duplicate_rows(df):
            errors.append("Duplicate Rows Found")

        if not check_price_logic(df):
            errors.append("Invalid Price Data")

        if not check_volume(df):
            errors.append("Invalid Volume Data")

    score = calculate_score(df, errors)
    status = get_status(score)

    return {
        "valid": status != "REJECT",
        "score": score,
        "status": status,
        "errors": errors,
    }


def validate_dataset(symbol, df):
    result = validate(df)

    report_path = generate_report(
        symbol=symbol,
        df=df,
        errors=result["errors"],
        score=result["score"],
        status=result["status"],
    )

    return {
        "symbol": symbol,
        "valid": result["valid"],
        "score": result["score"],
        "status": result["status"],
        "report": report_path,
        "errors": result["errors"],
    }
