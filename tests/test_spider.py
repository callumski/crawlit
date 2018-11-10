import os

from scrapy.http import TextResponse, Request

from crawlit.spiders.spider import CrawlitSpider
from crawlit.items import CrawlitItem


def mock_response_from_file(filename, url = None):
    """
    Build a Scrapy Response object based on a local HTML file
    :param filename: The path to the HTML file
    :return: A Scrapy TextResponse object for unit tests
    """

    if url is None:
        url = "http://www.example.com"
    request = Request(url)

    if filename[:1] != "/":
        test_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(test_dir, filename)
    else:
        file_path = filename

    with open(file_path, mode="r") as file:
        file_content = file.read()

    response = TextResponse(url=url, request=request, body=file_content, encoding='utf-8')
    return response


def test_linkless_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("linkless.html")))
    assert len(items[0]["internal_links"]) == 0
    assert len(items[0]["external_links"]) == 0

def test_oneimage_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("oneimage.html")))
    assert len(items[0]["internal_links"]) == 0
    assert len(items[0]["external_links"]) == 0
    images = items[0]["static_content"]
    assert len(images) == 1
    assert images[0] == "monalisa.jpg"

def test_one_internal_link_page():
    spider = CrawlitSpider()
    spider.allowed_domains=["http://www.example.com"]
    results = list(spider.parse(mock_response_from_file("oneinternal.html")))
    assert isinstance(results[0], CrawlitItem)
    assert len(results[0]["external_links"]) == 0
    internal_links = results[0]["internal_links"]
    assert internal_links == ["about_us.html"]
    assert isinstance(results[1], Request)


def test_one_external_link_page():
    spider = CrawlitSpider()
    results = list(spider.parse(mock_response_from_file("oneexternal.html")))
    assert len(results) == 1
    assert isinstance(results[0], CrawlitItem)
    external_links = results[0]["external_links"]
    assert external_links == ["http://www.example.com/interesting_page.html"]
    assert len(results[0]["internal_links"]) == 0