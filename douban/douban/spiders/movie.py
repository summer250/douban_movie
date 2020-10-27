# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Selector

from douban.items import DoubanItem

from scrapy_redis.spiders import RedisSpider

from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    headers = {
        'Cookie': 'bid=h_7m-JvTKR0; __gads=ID=fde61ed40e1b8559:T=1601735726:S=ALNI_Ma1BLMVhcNsQrm8sQQr3rNA6LF11g; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1602327248%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DK8RtefrXWKrvUsHZM5_D652aPXruDGN1ibhxJjOgHleaAXkfB5kBvqIT9qTfKNyY%26wd%3D%26eqid%3De8d6d645000c9596000000045f8192cc%22%5D; _pk_id.100001.4cf6=c36482012b1cfb02.1602327248.1.1602327248.1602327248.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.980966996.1602327248.1602327248.1602327248.1; __utmb=30149280.0.10.1602327248; __utmc=30149280; __utmz=30149280.1602327248.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1313248410.1602327248.1602327248.1602327248.1; __utmb=223695111.0.10.1602327248; __utmc=223695111; __utmz=223695111.1602327248.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=ewxpFSttmq0dUAtnFmzIxHhLJoP0wcze',
        'Host': 'movie.douban.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    }
    redis_key = 'myspider:start_urls'

    # 请求10页
    def start_requests(self):
        for page in range(0,10):
            page = 25*page
            start_urls = 'https://movie.douban.com/top250?start='+str(page)+'&filter='
            yield scrapy.Request(url=start_urls,callback=self.parse_page)

    # 获得详情页URL
    def parse_page(self, response):
        # print(response.text)
        selector = Selector(response)
        movie_urls = selector.xpath('//*[@class="hd"]/a/@href').extract()
        for movie_url in movie_urls:
            # print(movie_url)
            yield scrapy.Request(url=movie_url,headers=self.headers,callback=self.parse_detail_page)

    # 获得电影数据
    def parse_detail_page(self, response):
        item = DoubanItem()

        html = response.text
        selector = Selector(response)

        # 电影名
        movie_name = selector.xpath('//*[@property="v:itemreviewed"]/text()').extract()
        if movie_name:
            movie_name = "".join(movie_name)
            item['movie_name'] = movie_name

        # 导演
        director = selector.xpath('//*[@id="info"]/span[1]/span/a/text()').extract()
        if director:
            director = "".join(director)
            item['director'] = director

        # 编剧
        screenwriter = selector.xpath('//*[@id="info"]/span[2]/span/a/text()').extract()
        if screenwriter:
            screenwriter="".join(screenwriter)
            item['screenwriter'] = screenwriter

        # 主演
        tarring = selector.xpath('//*[@id="info"]/span[3]/span/a/text()').extract()
        if tarring:
            tarring = str(tarring)
            tarring= tarring.replace("[","").replace("]","").replace("'","")
            item['tarring'] = tarring

        # 类型
        types_of = selector.xpath('//*[@property="v:genre"]/text()').extract()
        if types_of:
            types_of = str(types_of)
            types_of = types_of.replace("[","").replace("]","").replace("'","")
            item['types_of'] = types_of

        # 制片国家/地区
        production_country = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', html)
        if production_country:
            production_country="".join(production_country)
            item['production_country'] = production_country

        # 语言
        language = re.findall('<span class="pl">语言:</span> (.*?)<br/>', html)
        if language:
            language="".join(language)
            item['language'] = language

        # 上映日期
        release_date = selector.xpath('//*[@property="v:initialReleaseDate"]/text()').extract()
        if release_date:
            release_date="".join(release_date)
            item['release_date'] = release_date

        # 片长
        length = selector.xpath('//*[@property="v:runtime"]/text()').extract()
        if length:
            length="".join(length)
            item['length'] = length

        # 又名
        also_known_as = re.findall('<span class="pl">又名:</span> (.*?)<br/>', html)
        if also_known_as:
            also_known_as="".join(also_known_as)
            item['also_known_as'] = also_known_as

        # 豆瓣评分
        score = selector.xpath('//*[@class="ll rating_num"]/text()').extract()
        if score:
            score="".join(score)
            item['score'] = score

        # 剧情简介
        synopsis = re.findall('<span class="all hidden">(.*?)</span>', html, re.S)
        if synopsis == []:
            synopsis = re.findall('<span property="v:summary" class="">(.*?)</span>',html,re.S)
        synopsis = str(synopsis)
        synopsis = ''.join(synopsis.split())
        synopsis = synopsis.replace(r"\n\u3000\u3000", "").replace(r"\n", "").replace(r"<br/>", "").replace("[", "").replace("]", "")
        item['synopsis'] = synopsis

        print(item)
        yield item











