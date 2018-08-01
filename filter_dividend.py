from pymongo import MongoClient
from pprint import pprint

db = MongoClient().belly

stocks = db.dividends.distinct("stock")

for stock in stocks:
    periods = db.dividends.find({"stock": stock}).distinct("period")
    if len(periods) < 5:
        print(f'stock {stock} does not have 5 years div payout')
        continue

    recent_periods = sorted(periods, reverse=True)[:5]
    non_continuous_pay_out = any((int(recent_periods[i]) - int(recent_periods[i + 1]) != 1) for i in range(4))

    if non_continuous_pay_out:
        print(f'stock {stock} stop pay dividend for some years')
        continue

    out = db.dividends.aggregate([
        {"$match": {"stock": stock}},
        {"$match": {"$or": [{"period": period} for period in recent_periods]}},
        {"$group": {"_id": {"stock": "$stock", "period": "$period"}, "total": {"$sum": "$dividend"}}},
        {"$sort": {"_id.period": -1}}
    ])

    decimal_div = [item['total'].to_decimal() for item in list(out)]
    pprint(decimal_div)
    passed = all((decimal_div[i] - decimal_div[i+1] >= 0)for i in range(4))
    print(f'stock {stock} result: {passed}')

# pprint.pprint(list(db.dividends.aggregate(pipeline)))

# for each stock
#    retrieve most recent 5 years dividend
#    if dividend increased on 4 out of 5 years, passed
