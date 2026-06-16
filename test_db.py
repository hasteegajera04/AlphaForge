import json

from database.queries import fetch_all


with open("config/stocks.json", "r") as file:
    data = json.load(file)

stocks = data["stocks"]

for stock in stocks:
    print("=" * 60)
    print("STOCK:", stock)
    print("=" * 60)

    rows = fetch_all(stock)

    for row in rows[:5]:
        print(row)

    print("Total rows:", len(rows))
    print()
