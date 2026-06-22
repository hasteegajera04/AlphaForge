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
from ingestion.storage import insert_validated_stock_data
from ingestion.database import init_database


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

    # Initialize database on first run
    init_database()
    
    # If validation passed, insert data into database
    db_status = "SKIPPED"
    if is_valid:
        db_result = insert_validated_stock_data(symbol, df, score, status)
        db_status = "SUCCESS" if db_result["success"] else "FAILED"

    output = {
        "symbol": symbol,
        "valid": is_valid,
        "score": score,
        "status": status,
        "report": report_path,
        "errors": errors,
        "db_status": db_status
    }

    return output
