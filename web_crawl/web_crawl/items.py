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
