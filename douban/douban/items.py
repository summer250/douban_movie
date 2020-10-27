# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    movie_name = scrapy.Field()  # 电影名
    director = scrapy.Field()   # 导演
    screenwriter = scrapy.Field()  # 编剧
    tarring = scrapy.Field()  # 主演
    types_of = scrapy.Field()  # 类型
    production_country = scrapy.Field()  # 制片国家/地区
    language = scrapy.Field()  # 语言
    release_date = scrapy.Field()  # 上映日期
    length = scrapy.Field()  # 片长
    also_known_as = scrapy.Field()  # 又名
    score = scrapy.Field()  # 豆瓣评分
    synopsis = scrapy.Field()  # 剧情简介

