import os

from scrapy.http import TextResponse, Request

from ..spiders.spider import CrawlitSpider


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
    assert len(items)[0]["links"] == 0

def test_oneimage_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("oneimage.html")))
    links = items[0]["links"]
    assert len(links) == 0
    images = items[0]["static_content"]
    assert len(images) == 1
    assert images[0] == "monalisa.jpg"


def test_onelink_page():
    spider = CrawlitSpider()
    items = spider.parse(mock_response_from_file("onelink.html"))
    links = list(items)[0]["links"]
    assert len(links) == 1
    assert links[0] == "about_us.html"


