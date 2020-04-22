import logging

from mongoengine import Document

from model.task import Task
from parser.dianping.comment_parser import CommentParser
from parser.dianping.detail_parser import DetailParser
from parser.dianping.list_parser import ListParser
from parser.sina_weibo.search_list_parser import SearchListParser
from parser.sina_weibo.topic_list_parser import TopicListParser
from parser.parser_builder import get_parser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MockParserDelegate:

    def save_content(self, content: Document, type_: str):
        logger.info(f'Save type {type_}, content {content}')

    # def append_url(self, url: str, type_: str, reference: str, metadata: dict):
    #     logger.info(f'Append url {url}, type {type_}, reference {reference}, metadata {metadata}')

    def append_request_task(self, task: Task):
        logger.info((f'Append task with url {task.url}, type {task.type_}, reference {task.reference},'
                     f' method {task.metadata}, body {task.body}, metadata {task.metadata}'))


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
    data = _load_html_file('./test_files/search_weibos.html')
    parser = SearchListParser(MockParserDelegate())
    parser.parse('https://s.weibo.com/weibo?q=%23%E7%96%AB%E6%83%85%E5%8F%AF%E8%83%BD%E5%AF%BC%E8%87%B420%E4%B8%87%E7%BE%8E%E5%9B%BD%E4%BA%BA%E6%AD%BB%E4%BA%A1%23', data)


def test_topic_list_parser():
    data = _load_html_file('./test_files/topic_list.html')
    parser = TopicListParser(MockParserDelegate())
    parser.parse('https://s.weibo.com/topic?q=%E7%96%AB%E6%83%85&pagetype=topic&topic=1&Refer=weibo_topic&page=2', data)


def test_cnr_search_list_parser():
    url = 'http://was.cnr.cn/'
    data = _load_html_file('./test_files/cnr_list.html')
    parser = get_parser(url, MockParserDelegate())
    parser.parse(url, data, {})


def test_people_search_list_parser():
    url = 'http://search.people.com.cn/cnpeople/news/getNewsResult.jsp'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/people_list.html', 'gbk')
    parser = get_parser(url, MockParserDelegate())
    parser.parse(task, data)


def test_china_news_search_list_parser():
    url = 'http://sou.chinanews.com/search.do'
    task = Task(url, '', '', method='POST')
    data = _load_html_file('./test_files/china_news_list.html')
    parser = get_parser(url, MockParserDelegate())
    parser.parse(task, data)


def test_sina_news_search_list_parser():
    url = 'https://search.sina.com.cn/?q=%E7%96%AB%E6%83%85&range=all&c=news&sort=time'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/sina_news_list.html')
    parser = get_parser(url, MockParserDelegate())
    parser.parse(task, data)


def _load_html_file(filepath: str, encodeing='utf-8'):
    with open(filepath, 'r', encoding=encodeing) as html_file:
        data = html_file.read()
    return data
