import json
from pprint import pprint
from decimal import *
from collections import defaultdict
from collections import OrderedDict
import re

data_file = open('dividends.json')
records = json.load(data_file)

processedRecords = list()
for record in records:
    divPattern = re.compile(r'.*HKD ([0-9\.]+).*')
    divMatch = divPattern.match(record['dividend'])
    divNum = Decimal(divMatch.group(1))

    yPattern = re.compile(r'([0-9]{4})\/.*')
    yMatch = yPattern.match(record['period'])
    yValue = yMatch.group(1)

    processedRecords.append((yValue, divNum))

result = defaultdict(Decimal)

for year, div in processedRecords:
    result[year] += div

sortedResult = OrderedDict(reversed(sorted(result.items())))
pprint(sortedResult)

increments = [
    sortedResult['2017'] - sortedResult['2016'],
    sortedResult['2016'] - sortedResult['2015'],
    sortedResult['2015'] - sortedResult['2014'],
    sortedResult['2014'] - sortedResult['2013'],
    sortedResult['2013'] - sortedResult['2012']
]

passed = all(i >= 0 for i in increments)

pprint(increments)

print(f"passed test = {passed}")
