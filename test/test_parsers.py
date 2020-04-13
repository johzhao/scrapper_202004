import logging

from mongoengine import Document

from parser.dianping.comment_parser import CommentParser
from parser.dianping.detail_parser import DetailParser
from parser.dianping.list_parser import ListParser
from parser.sina_weibo.search_list_parser import SearchListParser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MockParserDelegate:

    def save_content(self, content: Document, type_: str):
        logger.info(f'Save type {type_}, content {content}')
        pass

    def append_url(self, url: str, type_: str, reference: str):
        logger.info(f'Append url {url}, type {type_}, reference {reference}')
        pass


def test_list_parser():
    with open('./test_files/shop_list.html', 'r') as html_file:
        data = html_file.read()
    parser = ListParser(MockParserDelegate())
    parser.parse('https://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F', data)


def test_detail_parser():
    with open('./test_files/shop_detail.html', 'r') as html_file:
        data = html_file.read()
    parser = DetailParser(MockParserDelegate())
    parser.parse('https://www.dianping.com/shop/90556783', data)


def test_comment_parser():
    with open('./test_files/shop_reviews.html', 'r') as html_file:
        data = html_file.read()
    parser = CommentParser(MockParserDelegate())
    parser.parse('https://www.dianping.com/shop/90556783/review_all', data)


def test_weibo_parser():
    data = _load_html_file('./test_files/test_weibo.html')
    parser = SearchListParser(MockParserDelegate())
    parser.parse('https://s.weibo.com/weibo?q=%23%E7%96%AB%E6%83%85%E5%8F%AF%E8%83%BD%E5%AF%BC%E8%87%B420%E4%B8%87%E7%BE%8E%E5%9B%BD%E4%BA%BA%E6%AD%BB%E4%BA%A1%23', data)


def _load_html_file(filepath: str):
    with open(filepath, 'r', encoding='utf8') as html_file:
        data = html_file.read()
    return data
