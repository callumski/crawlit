# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlitItem(scrapy.Item):
    """Class to hold results of CrawlitSpider parsing."""

    url = scrapy.Field()
    static_content = scrapy.Field()
    internal_links = scrapy.Field()
    external_links = scrapy.Field()
