from validation.rules import (
    check_duplicate_rows,
    check_empty,
    check_missing_values,
    check_price_logic,
    check_required_columns,
    check_volume,
)
from validation.score import calculate_score, get_status


def validate(df):
    errors = []

    if not check_empty(df):
        errors.append("Empty DataFrame")

    has_required_columns = check_required_columns(df)
    if not has_required_columns:
        errors.append("Missing Required Columns")

    if has_required_columns:
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
