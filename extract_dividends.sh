#!/bin/bash

[ -e out/dividends.json ] && rm out/dividends.json

python3 -m scrapy runspider dividend_spider.py -o out/dividends.json --logfile logs/run.log