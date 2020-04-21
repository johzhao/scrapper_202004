import logging
import urllib.parse

from mongoengine import connect

import config
from export.export import export_task_3
from model.sina_topic import SinaTopic

log_format = ' %(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

from scheduler.scheduler import Scheduler

logger = logging.getLogger(__name__)

KEYWORDS = [
    '新冠',
    '肺炎',
    '武汉',
    'COVID-19',
    '冠状病毒',
    '疫情',
]


def add_topic_search_tasks(scheduler: Scheduler):
    for index in range(50):
        url = ''
        reference_url = ''
        keyword = urllib.parse.quote(config.KEYWORD)
        if index == 0:
            url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic'
        else:
            url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic&page={index + 1}'
            reference_url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic&page={index}'

        scheduler.append_url(url, '', reference_url)
    pass


def add_weibo_hot_search_tasks(scheduler: Scheduler):
    for index in range(50):
        keyword = urllib.parse.quote(config.KEYWORD)
        if index == 0:
            url = f'https://s.weibo.com/weibo?q={keyword}&xsort=hot&suball=1&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g'
            reference_url = ''
        else:
            url = f'https://s.weibo.com/weibo?q={keyword}&xsort=hot&suball=1&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g&page={index}'
            reference_url = f'https://s.weibo.com/weibo?q={keyword}&xsort=hot&suball=1&timescope=custom:2020-01-10-0:2020-04-10-23&Refer=g&page={index - 1}'
        scheduler.append_url(url, '', reference_url)


def add_topic_detail_tasks(scheduler: Scheduler):
    connect(config.MONGO_DATABASE, host=config.MONGO_HOST, port=config.MONGO_PORT)
    urls = set()
    for topic in SinaTopic.objects:
        if topic.url:
            urls.add(topic.url)

    for url in urls:
        scheduler.append_url(url, '', '')


def add_cnr_search_task(scheduler: Scheduler):
    for keyword in KEYWORDS:
        search_key = urllib.parse.quote(keyword)
        url = f'http://was.cnr.cn/was5/web/search?page=2&channelid=234439&searchword={search_key}&keyword={search_key}&orderby=LIFO&was_custom_expr=%28{search_key}%29&perpage=10&outlinepage=1&searchscope=&timescope=&timescopecolumn=&orderby=LIFO&andsen=&total=&orsen=&exclude='
        scheduler.append_url(url, '', '', {
            'keyword': keyword
        })


def export():
    export_task_3('./output/task_1_2.xlsx')
    pass


def main():
    scheduler = Scheduler()
    # scheduler.append_url('https://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F', 'list', '')

    # add_topic_search_tasks(scheduler)
    # add_topic_detail_tasks(scheduler)
    # add_weibo_hot_search_tasks(scheduler)
    # add_cnr_search_task(scheduler)

    scheduler.start()
    scheduler.join()

    # export()


if __name__ == '__main__':
    main()
