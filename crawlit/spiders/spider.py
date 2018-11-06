# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse


class SpiderSpider(Spider):
    name = 'spider'

    def start_requests(self):
        url = getattr(self, 'url', None)
        domain = urlparse(url).netloc
        self.allowed_domains = [domain]

        if url is not None:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        print( response.url )
