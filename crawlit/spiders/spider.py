import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse
from ..items import CrawlitItem


class CrawlitSpider(Spider):
    """
    Simple web crawler, limited to one domain. Given a starting URL it will visit all pages within the domain, but not
    follow the links to external sites such as Google or Twitter.

    It collects a list of items with url, internal links, external links and static content.
    """

    name = 'spider'
    allowed_domains = []
    parsed_pages = []

    def start_requests(self):
        url = getattr(self, 'url', None)
        domain = urlparse(url).netloc
        self.allowed_domains = [domain]

        if url is not None:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        self.parsed_pages.append(response.url)
        internal_links = []
        external_links = []

        urls = response.xpath('//a/@href').extract()

        for url in urls:
            netloc = urlparse(url).netloc
            if netloc == '' or netloc in self.allowed_domains:
                internal_links.append(url)
            else:
                external_links.append(url)

        item = CrawlitItem()
        item['url'] = response.url
        item['static_content'] = response.xpath('//*[contains(@src, ".")]').xpath('@src').extract()
        item['internal_links'] = internal_links
        item['external_links'] = external_links
        yield item

        for url in internal_links:
            if url[:1] != "#" and url not in self.parsed_pages:
                yield response.follow(url, callback=self.parse)
