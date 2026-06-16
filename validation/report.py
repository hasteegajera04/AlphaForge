import os

def generate_report(symbol, df, errors, score, status):

    os.makedirs("reports/validation", exist_ok=True)

    path = f"reports/validation/{symbol}_validation_report.txt"

    with open(path, "w") as f:

        f.write(f"Stock: {symbol}\n\n")
        f.write(f"Rows: {len(df)}\n\n")

        f.write("Errors:\n")
        if errors:
            for e in errors:
                f.write(f"- {e}\n")
        else:
            f.write("None\n")

        f.write(f"\nScore: {score}\n")
        f.write(f"Status: {status}\n")

    return path
