# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
from decimal import *
from bson.decimal128 import Decimal128


class DividendsMongoPipeline(object):
    collection_name = 'dividends'

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client['belly']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for record in item['records']:
            hkd_pattern = re.compile(r'.*HKD ([0-9\.]+).*')
            rmb_pattern = re.compile(r'.*RMB ([0-9\.]+).*')
            hkd_match = hkd_pattern.match(record['dividend'])
            rmb_match = rmb_pattern.match(record['dividend'])
            if hkd_match:
                record['dividend'] = str(Decimal(hkd_match.group(1)))
            elif rmb_match:
                record['dividend'] = str(Decimal(rmb_match.group(1)) * Decimal('1.14'))
            else:
                record['dividend'] = str(Decimal(0))

            self.db[self.collection_name].insert_one(dict(record))
        return item
