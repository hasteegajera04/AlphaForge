from .rules import *


def validate(df):

    errors = []

    if not check_empty(df):
        errors.append("Empty DataFrame")

    if not check_required_columns(df):
        errors.append("Missing Required Columns")

    if not check_missing_values(df):
        errors.append("Missing Values Found")

    if not check_duplicate_rows(df):
        errors.append("Duplicate Rows Found")

    if not check_price_logic(df):
        errors.append("Invalid Price Data")

    if not check_volume(df):
        errors.append("Invalid Volume Data")

    if errors:
        print("Validation Failed")

        for error in errors:
            print(error)

        return False

    print("Validation Passed")
    return True