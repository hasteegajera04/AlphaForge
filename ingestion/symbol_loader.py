import json

from config.db_config import STOCKS_FILE


def load_symbols():
    with STOCKS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["stocks"]
