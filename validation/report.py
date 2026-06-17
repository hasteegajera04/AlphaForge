from config.db_config import REPORT_DIR


def generate_report(symbol, df, errors, score, status):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    path = REPORT_DIR / f"{symbol}_validation_report.txt"

    with path.open("w", encoding="utf-8") as file:
        file.write(f"Stock: {symbol}\n\n")
        file.write(f"Rows: {len(df)}\n\n")

        file.write("Errors:\n")
        if errors:
            for error in errors:
                file.write(f"- {error}\n")
        else:
            file.write("None\n")

        file.write(f"\nScore: {score}\n")
        file.write(f"Status: {status}\n")

    return str(path)
