import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse
from ..items import CrawlitItem


class CrawlitSpider(Spider):
    name = 'spider'

    def start_requests(self):
        url = getattr(self, 'url', None)
        domain = urlparse(url).netloc
        self.allowed_domains = [domain]

        if url is not None:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        links = []
        for url in response.xpath('//a/@href').extract():
            links.append(url)


        item = CrawlitItem()
        item['url'] = response.url
        item['static_content'] = response.xpath('//*[contains(@src, ".")]').xpath('@src').extract()
        item['links'] = links
        yield item