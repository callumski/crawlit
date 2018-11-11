import os

from scrapy.http import TextResponse, Request

from crawlit.spiders.spider import CrawlitSpider
from crawlit.items import CrawlitItem


def mock_response_from_file(filename, url=None):
    """ Build a Scrapy Response object based on a local HTML file

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

    response = TextResponse(url=url, request=request, body=file_content,
                            encoding='utf-8')
    return response


def test_linkless_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("html/linkless.html")))
    assert len(items) == 1
    assert len(items[0]["internal_links"]) == 0
    assert len(items[0]["external_links"]) == 0


def test_oneimage_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("html/oneimage.html")))
    assert len(items[0]["internal_links"]) == 0
    assert len(items[0]["external_links"]) == 0
    images = items[0]["static_content"]
    assert len(images) == 1
    assert images[0] == "monalisa.jpg"


def test_one_internal_link_page():
    spider = CrawlitSpider()
    spider.allowed_domains = ["www.example.com"]
    results = list(
        spider.parse(mock_response_from_file("html/oneinternal.html")))
    assert isinstance(results[0], CrawlitItem)
    assert len(results[0]["external_links"]) == 0
    internal_links = results[0]["internal_links"]
    assert internal_links == ["about_us.html"]
    assert isinstance(results[1], Request)


def test_one_internal_link_full_url_page():
    spider = CrawlitSpider()
    spider.allowed_domains = ["www.example.com"]
    results = list(spider.parse(
        mock_response_from_file("html/alternative_one_internal.html")))
    assert isinstance(results[0], CrawlitItem)
    assert len(results[0]["external_links"]) == 0
    internal_links = results[0]["internal_links"]
    assert internal_links == ["http://www.example.com/about_us.html"]
    assert isinstance(results[1], Request)


def test_one_external_link_page():
    spider = CrawlitSpider()
    spider.allowed_domains = ["www.example.com"]
    results = list(
        spider.parse(mock_response_from_file("html/oneexternal.html")))
    assert len(results) == 1
    assert isinstance(results[0], CrawlitItem)
    external_links = results[0]["external_links"]
    assert external_links == [
        "http://www.interesting.com/interesting_page.html"]
    assert len(results[0]["internal_links"]) == 0


def test_html5_vid_page():
    spider = CrawlitSpider()
    items = list(spider.parse(mock_response_from_file("html/html5video.html")))
    assert len(items[0]["internal_links"]) == 0
    assert len(items[0]["external_links"]) == 0
    videos = items[0]["static_content"]
    assert len(videos) == 2
    assert "movie.mp4" in videos
    assert "movie.ogg" in videos


def test_onelocationhash_within_page():
    spider = CrawlitSpider()
    spider.allowed_domains = ["www.example.com"]
    results = list(
        spider.parse(mock_response_from_file("html/onelocationhash.html")))
    assert len(results) == 1
    assert isinstance(results[0], CrawlitItem)
    assert len(results[0]["external_links"]) == 0
    internal_links = results[0]["internal_links"]
    assert internal_links == ["#about_us"]


def test_remove_invalid_javascript_call_links():
    spider = CrawlitSpider()
    links = spider.remove_invalid_links(
        ["javascript:void(0)", "javascript:void(0);"])
    assert links == []
