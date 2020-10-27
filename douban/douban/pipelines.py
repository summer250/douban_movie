# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class DoubanPipeline:
    collection = "douban"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = {
            '电影名': item["movie_name"],
            '导演': item["director"],
            '编剧': item["screenwriter"],
            '主演': item["tarring"],
            '类型': item["types_of"],
            '制片国家/地区': item["production_country"],
            '语言': item["language"],
            '上映日期': item["release_date"],
            '片长': item["length"],
            '又名': item["also_known_as"],
            '豆瓣评分': item["score"],
            '剧情简介': item["synopsis"],
        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item
