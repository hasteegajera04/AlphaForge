import json

def load_symbols():

    with open("config/stocks.json", "r") as file:
        data = json.load(file)

    return data["stocks"]