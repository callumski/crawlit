import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlparse
from ..items import CrawlitItem

"""CrawlitSpider: A simple web crawler, limited to one domain.

    Crawls one domain to find links and static content.
"""

class CrawlitSpider(Spider):
    """A simple web crawler, limited to one domain.

    Given a starting URL it will
    visit all pages within the domain, but not
    follow the links to external sites such as Google or Twitter.

    It collects a list of items with url, internal links, external links and
    static content.
    """

    name = 'spider'
    allowed_domains = []
    parsed_pages = []

    def start_requests(self):
        """
        Provide the starting URL.

        Parse the 'url' command line argument to serve as the root domain for
        the spider. Set it as the only domain in allowed_domains.
        :return: a list of URL strings (containing only the root domain for the
        spider)
        """
        url = getattr(self, 'url', None)
        domain = urlparse(url).netloc
        self.allowed_domains = [domain]

        if url is not None:
            yield scrapy.Request(url, self.parse)

    def remove_invalid_links(self, links):
        """Remove javascript method calls from a list of URL strings."""
        return [url for url in links if url[:18] != "javascript:void(0)"]

    def parse(self, response):
        """
        Parse a Scrapy Response Object for links and static content.

        Parses the Response object and extracts a list of all the links to
        other pages or static content. Yields a CrawlitItem containing those
        links in the correct fields and a Scrapy Request object for each link
        to another page on the same domain and has yet to be parsed.

        :param response: A Scrapy Response object
        :return: a list containing 1 CrawlitItem objects and none of more
        Request objects
        """
        self.parsed_pages.append(response.url)
        internal_links = []
        external_links = []

        urls = self.remove_invalid_links(response.xpath('//a/@href').extract())

        for url in urls:
            netloc = urlparse(url).netloc
            print("url: {}   netloc: {}".format(url, netloc))
            if netloc == '' or netloc in self.allowed_domains:
                internal_links.append(url)
            else:
                external_links.append(url)

        item = CrawlitItem()
        item['url'] = response.url
        item['static_content'] = response.xpath(
            '//*[contains(@src, ".")]').xpath('@src').extract()
        item['internal_links'] = internal_links
        item['external_links'] = external_links
        yield item

        for url in internal_links:
            if url[:1] != "#" and url not in self.parsed_pages:
                yield response.follow(url, callback=self.parse)
