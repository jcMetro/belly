from decimal import *
from pymongo import MongoClient
from pprint import pprint
import csv
import numpy as np


def filter_increase_div_stock(the_stocks):
    results = []
    for stockItem in the_stocks:
        periods = db.dividends.find({"stock": stockItem}).distinct("period")

        recent_periods = sorted(periods, reverse=True)

        if recent_periods[0] == '2018':
            recent_periods = recent_periods[1:]

        if len(recent_periods) < 5:
            continue

        recent_periods = recent_periods[:5]

        non_continuous_pay_out = any((int(recent_periods[i]) - int(recent_periods[i + 1]) != 1) for i in range(4))

        if non_continuous_pay_out:
            continue

        out = db.dividends.aggregate([
            {"$match": {"stock": stockItem}},
            {"$match": {"$or": [{"period": period} for period in recent_periods]}},
            {"$group": {"_id": {"stock": "$stock", "period": "$period"}, "total": {"$sum": "$dividend"}}},
            {"$sort": {"_id.period": -1}}
        ])

        decimal_div = [item['total'].to_decimal() for item in list(out)]
        differences = (decimal_div[i] - decimal_div[i + 1] for i in range(4))
        number_of_negative_diff = sum(1 for diff in differences if diff < 0)

        passed = number_of_negative_diff <= 1
        if passed:
            results.append(stockItem)

    return results


def filter_valid_stock(the_stocks):
    results = []
    for stock in the_stocks:
        e_records = list(db.earning.find({"stock": stock}).sort("period", -1))
        latest_dividend_payout = e_records[0]['dividend_payout']
        if not latest_dividend_payout:
            continue
        if Decimal(latest_dividend_payout) >= 100:
            continue

        results.append(stock)
    return results


if __name__ == "__main__":
    db = MongoClient().belly
    stocks = db.dividends.distinct("stock")
    increase_div_stocks = filter_increase_div_stock(stocks)
    valid_stocks = filter_valid_stock(increase_div_stocks)

    pprint(valid_stocks)

    with open('final_output.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for stock_item in valid_stocks:
            db_item = db.stock.find({"code": stock_item}).next()
            latest_dividend = db.earning.find({"stock": stock_item}).sort("period", -1).next()['dividend']
            dividends = [Decimal(str(item['dividend']))
                         for item in list(db.earning.find({"stock": stock_item}).sort("period", -1))]
            dividends = dividends[:5]
            growths = [(1 + (dividends[i] - dividends[i + 1]) / dividends[i + 1]) for i in range(4)]
            avg_growth = (np.array(growths).prod() ** (Decimal('1.0') / len(growths))) - 1

            if avg_growth < 0:
                continue

            writer.writerow([stock_item, str(db_item['last_price']), str(latest_dividend), avg_growth])
