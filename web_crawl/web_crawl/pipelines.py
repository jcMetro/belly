# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

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
            self.db[self.collection_name].insert_one(dict(record))
        return item
