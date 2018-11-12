# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DividendRecord(scrapy.Item):
    stock = scrapy.Field()
    period = scrapy.Field()
    dividend = scrapy.Field()


class RoeRecord(scrapy.Item):
    stock = scrapy.Field()
    period = scrapy.Field()
    debt_to_equity = scrapy.Field()
    roe = scrapy.Field()


class EarningRecord(scrapy.Item):
    stock = scrapy.Field()
    period = scrapy.Field()
    earning = scrapy.Field()
    dividend = scrapy.Field()
    dividend_payout = scrapy.Field()
    eps_growth = scrapy.Field()
