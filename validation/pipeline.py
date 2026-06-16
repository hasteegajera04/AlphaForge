# from validation.validator import validate
# from validation.report import generate_report


# def validate_dataset(symbol, df):
#     result = validate(df)

#     report_path = generate_report(
#         symbol,
#         df,
#         result["errors"],
#         result["score"],
#         result["status"],
#     )

#     return {
#         "symbol": symbol,
#         "valid": result["valid"],
#         "score": result["score"],
#         "status": result["status"],
#         "report": report_path,
#         "errors": result["errors"],
#     }

from validation.validator import validate
from validation.report import generate_report


def validate_dataset(symbol, df):

    result = validate(df)

    errors = result["errors"]
    score = result["score"]
    status = result["status"]
    is_valid = result["valid"]

    report_path = generate_report(
        symbol=symbol,
        df=df,
        errors=errors,
        score=score,
        status=status
    )

    output = {
        "symbol": symbol,
        "valid": is_valid,
        "score": score,
        "status": status,
        "report": report_path,
        "errors": errors
    }

    return output
