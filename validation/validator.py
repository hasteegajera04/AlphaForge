from .rules import *


def validate(df):

    print("Validation Started ")

    if not check_empty(df):
        print("FAIL : Empty DataFrame")
        return False

    if not check_required_columns(df):
        print("FAIL : Missing Required Columns")
        return False

    if not check_missing_values(df):
        print("FAIL : Missing Values Found")
        return False

    if not check_duplicate_rows(df):
        print("FAIL : Duplicate Rows Found")
        return False

    if not check_price_logic(df):
        print("FAIL : Invalid Price Data")
        return False

    if not check_volume(df):
        print("FAIL : Invalid Volume Data")
        return False

    print("Validation Passed")
    return True