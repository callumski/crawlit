import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse


class CrawlitSpider(Spider):
    name = 'spider'

    def start_requests(self):
        url = getattr(self, 'url', None)
        domain = urlparse(url).netloc
        self.allowed_domains = [domain]

        if url is not None:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        pass
