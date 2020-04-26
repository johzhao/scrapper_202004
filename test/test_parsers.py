import logging

from model.parsed_result_item import ParsedResultItem
from model.task import Task
from parser.parser_builder import get_parser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_list_parser():
    data = _load_html_file('./test_files/shop_list.html')
    url = 'https://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F'
    task = Task(url, '', '')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_detail_parser():
    data = _load_html_file('./test_files/shop_detail.html')
    url = 'https://www.dianping.com/shop/90556783'
    task = Task(url, '', '')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_comment_parser():
    with open('./test_files/shop_reviews.html', 'r') as html_file:
        data = html_file.read()
    url = 'https://www.dianping.com/shop/90556783/review_all'
    task = Task(url, '', '')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_weibo_parser():
    data = _load_html_file('./test_files/search_weibos.html')
    url = 'https://s.weibo.com/weibo?q=%23%E7%96%AB%E6%83%85%E5%8F%AF'
    task = Task(url, '', '')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_topic_list_parser():
    data = _load_html_file('./test_files/topic_list.html')
    url = 'https://s.weibo.com/topic?q=%E7%96%AB%E6%83%85&pagetype=topic&topic=1&Refer=weibo_topic&page=2'
    task = Task(url, '', '')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_cnr_search_list_parser():
    url = 'http://was.cnr.cn/'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/cnr_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_xinhua_search_list_parser():
    url = f'http://so.news.cn/getNews'
    params = {
        'keyword': '疫情',
        'curPage': 0,
        'sortField': 0,
        'searchFields': 1,
        'lang': 'cn',
    }
    task = Task(url, '', '', params=params)
    data = _load_html_file('./test_files/xinhua_list.json')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_people_search_list_parser():
    url = 'http://search.people.com.cn/cnpeople/news/getNewsResult.jsp'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/people_list.html', 'gbk')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_china_news_search_list_parser():
    url = 'http://sou.chinanews.com/search.do'
    task = Task(url, '', '', method='POST')
    data = _load_html_file('./test_files/china_news_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_sina_news_search_list_parser():
    url = 'https://search.sina.com.cn/?q=%E7%96%AB%E6%83%85&range=all&c=news&sort=time'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/sina_news_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_gov_search_list_parser():
    url = 'http://sousuo.gov.cn/s.htm?t=govall&q=%E7%96%AB%E6%83%85'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/gov_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_china_cdc_search_list_parser():
    url = 'http://www.chinacdc.cn/was5/web/search'
    params = {
        'page': 2,
        'channelid': 233877,
        'searchword': '疫情',
        'keyword': '疫情',
        'orderby': '-日期',
        'perpage': 10,
        'outlinepage': 5,
    }
    task = Task(url, '', '', params=params)
    data = _load_html_file('./test_files/china_cdc_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_china_list_parser():
    url = 'http://search1.china.com.cn/search/searchcn.jsp'
    body = {
        'searchText': '新冠',
        'submit': '%E6%90%9C%E7%B4%A2',
        'nodeid': '',
        'strKeyword': '',
        'strUrl': '',
        'strNodename': '',
        'sourcename=': '',
        'LateTag': 1,
        'strFromdate': '',
        'strTodate': '',
        'strSortBy': 0,
        'server': 1,
    }
    task = Task(url, '', '', method='POST', body=body)
    data = _load_html_file('./test_files/china_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_cctv_list_parser():
    url = 'https://search.cctv.com/search.php?qtext=%E6%96%B0%E5%86%A0&sort=relevance&type=web'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/cctv_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def test_the_paper_list_parser():
    url = 'https://www.thepaper.cn/searchResult.jsp?inpsearch=%E7%96%AB%E6%83%85'
    task = Task(url, '', '')
    data = _load_html_file('./test_files/the_paper_list.html')
    parser = get_parser(url)
    _parse(parser, task, data)


def _load_html_file(filepath: str, encodeing='utf-8'):
    with open(filepath, 'r', encoding=encodeing) as html_file:
        data = html_file.read()
    return data


def _parse(parser, task, data):
    for item in parser.parse(task, data):
        if isinstance(item, Task):
            logger.info((f'Append task with url {task.url}, type {task.type_}, reference {task.reference}, '
                         f'method {task.method}, params {task.params}, body {task.body}, metadata {task.metadata}'))
        elif isinstance(item, ParsedResultItem):
            logger.info(f'Save parsed item {item}')
        else:
            raise Exception(f'Unsupported parse result: class={item.__class__}')
