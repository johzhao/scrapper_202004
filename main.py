import logging
import urllib.parse

from mongoengine import connect

import config
from export.export_task_4 import export_task_4
from export.export_task_4_weibo import export_task_4_weibo
from model.sina_topic_v2 import WeiboTopicItem
from model.task import Task

log_format = ' %(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

from scheduler.scheduler import Scheduler

logger = logging.getLogger(__name__)


def add_topic_search_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_keyword = urllib.parse.quote(keyword)
        for index in range(50):
            reference_url = ''
            if index == 0:
                url = f'https://s.weibo.com/topic?q={search_keyword}&pagetype=topic&topic=1&Refer=weibo_topic'
            else:
                url = f'https://s.weibo.com/topic?q={search_keyword}&pagetype=topic&topic=1&Refer=weibo_topic' \
                      f'&page={index + 1}'
                reference_url = f'https://s.weibo.com/topic?q={search_keyword}&pagetype=topic&topic=1' \
                                f'&Refer=weibo_topic&page={index}'

            scheduler.append_request_task(Task(url, '', reference_url, metadata={
                'keyword': keyword
            }))


def add_weibo_hot_search_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_keyword = urllib.parse.quote(keyword)
        for index in range(50):
            if index == 0:
                url = (f'https://s.weibo.com/weibo?q={search_keyword}&xsort=hot&suball=1'
                       f'&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g')
                reference_url = ''
            else:
                url = (f'https://s.weibo.com/weibo?q={search_keyword}&xsort=hot&suball=1'
                       f'&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g&page={index}')
                reference_url = (f'https://s.weibo.com/weibo?q={search_keyword}&xsort=hot&suball=1'
                                 f'&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g&page={index - 1}')
            scheduler.append_request_task(Task(url, '', reference_url, metadata={
                'keyword': keyword
            }))


# def add_topic_detail_tasks(scheduler: Scheduler):
#     connect(config.MONGO_DATABASE, host=config.MONGO_HOST, port=config.MONGO_PORT)
#     urls = set()
#     for topic in SinaTopic.objects:
#         if topic.url:
#             urls.add(topic.url)
#
#     for url in urls:
#         scheduler.append_url(url, '', '')


def add_cnr_search_task(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = (f'http://was.cnr.cn/was5/web/search?page=2&channelid=234439&searchword={search_key}'
               f'&keyword={search_key}&orderby=LIFO&was_custom_expr=%28{search_key}%29&perpage=10'
               f'&outlinepage=1&searchscope=&timescope=&timescopecolumn=&orderby=LIFO&andsen=&total=&orsen=&exclude=')
        scheduler.append_request_task(Task(url, '', '', metadata={
            'keyword': keyword
        }))


def add_xinhua_search_task(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'http://so.news.cn/getNews'
        params = {
            'keyword': search_key,
            'curPage': 0,
            'sortField': 0,
            'searchFields': 1,
            'lang': 'cn',
        }
        scheduler.append_request_task(Task(url, '', '', params=params, metadata={
            'keyword': keyword
        }))


def add_people_search_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword, encoding='gbk')
        url = (f'http://search.people.com.cn/cnpeople/search.do?pageNum=2&keyword={search_key}'
               f'&siteName=news&facetFlag=true&nodeType=belongsId&nodeId=0')
        body = {
            'keyword': search_key,
            'pageNum': 1,
            'siteName': 'news',
            'facetFlag': True,
            'nodeType': 'belongsId',
            'nodeId': 0,
            'pageCode': '',
            'originName': '',
        }
        scheduler.append_request_task(Task(url, '', '', method='POST', body=body, metadata={
            'keyword': keyword
        }))


def add_china_news_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'http://sou.chinanews.com/search.do'
        body = {
            'q': search_key,
        }
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', method='POST', body=body, metadata=metadata))


def add_sina_news_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'https://search.sina.com.cn/?q={search_key}&range=all&c=news&sort=time'
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def add_gov_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'http://sousuo.gov.cn/s.htm?t=govall&q={search_key}'
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def add_china_cdc_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = (f'http://www.chinacdc.cn/was5/web/search?searchword={search_key}&channelid=233877&timescope=&'
               f'timescopecolumn=&orderby=-%E6%97%A5%E6%9C%9F&perpage=10&searchscope=')
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def add_china_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = 'http://search1.china.com.cn/search/searchcn.jsp'
        body = {
            'searchText': search_key,
            'submit': '搜索',
            'nodeid': '',
            'strKeyword': '',
            'strUrl': '',
            'strNodename': '',
            'sourcename=': '',
            'LateTag': '',
            'strFromdate': '',
            'strTodate': '',
            'strSortBy': 0,
            'server': 1,
        }
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', method='POST', body=body, metadata=metadata))


def add_cctv_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = (f'https://search.cctv.com/search.php?qtext={search_key}&sort=relevance&type=web&vtime='
               f'&datepid=1&channel=&page=1')
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def add_weibo_topic_list_tasks(scheduler: Scheduler):
    for keyword in config.KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'https://s.weibo.com/topic?q={search_key}&pagetype=topic&topic=1&Refer=weibo_topic'
        metadata = {
            'keyword': keyword,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def add_weibo_info_tasks(scheduler: Scheduler):
    for item in WeiboTopicItem.objects().order_by('title'):
        search_key = urllib.parse.quote(item.title)
        url = f'https://m.s.weibo.com/ajax_topic/trend?q={search_key}&time=30d'
        metadata = {
            'keyword': item.keyword,
            'title': item.title,
        }
        scheduler.append_request_task(Task(url, '', '', metadata=metadata))


def export():
    # export_task_3('./output/task_1_2.xlsx')
    # export_task_4('./output/task_4_v2.xlsx')
    export_task_4_weibo('./output/task_4_weibo.xlsx')


def main():
    connect(config.MONGO_DATABASE, host=config.MONGO_HOST, port=config.MONGO_PORT)

    scheduler = Scheduler()

    # add_topic_search_tasks(scheduler)
    # add_topic_detail_tasks(scheduler)
    # add_weibo_hot_search_tasks(scheduler)
    # add_cnr_search_task(scheduler)
    # add_xinhua_search_task(scheduler)
    # add_people_search_tasks(scheduler)
    # add_china_news_tasks(scheduler)
    # add_sina_news_tasks(scheduler)
    # add_gov_tasks(scheduler)
    # add_china_cdc_tasks(scheduler)
    # add_china_tasks(scheduler)
    # add_cctv_tasks(scheduler)
    # add_weibo_topic_list_tasks(scheduler)
    # add_weibo_info_tasks(scheduler)

    # scheduler.start()
    # scheduler.join()

    export()


if __name__ == '__main__':
    main()
