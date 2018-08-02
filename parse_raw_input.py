import csv
from pprint import pprint
import re
from pymongo import MongoClient
from bson.decimal128 import *


class StockItem:
    def __init__(self, code, name, last_price, dividend_yield):
        self.code = code
        self.name = name
        self.last_price = last_price
        self.dividend_yield = dividend_yield

    def __repr__(self):
        return str(self.__dict__)


def create_stock_item(row):
    code = row[0]
    name = row[1]

    last_price_match = re.compile(r'HK\$([0-9\.]*)').match(row[2])
    last_price = Decimal128(last_price_match.group(1))

    div_yield_match = re.compile(r'([0-9\.]*)%').match(row[6])
    if div_yield_match:
        dividend_yield = Decimal128(div_yield_match.group(1))
    else:
        dividend_yield = Decimal128("0")

    return StockItem(code, name, last_price, dividend_yield)


if __name__ == "__main__":
    rows = []
    with open('raw_input/input.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    valid_rows = [row for row in rows[1:] if not row[0].startswith('Suspended')]
    stock_items = [create_stock_item(row) for row in valid_rows]
    pprint(stock_items)

    db = MongoClient().belly
    for stock_item in stock_items:
        db['stock'].insert_one(vars(stock_item))
