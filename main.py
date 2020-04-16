import logging

from mongoengine import connect
import urllib.parse

import config
from export.export import export_shops_to_excel, export_reviews_to_excel
from model.sina_topic import SinaTopic

log_format = ' %(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

from scheduler.scheduler import Scheduler

logger = logging.getLogger(__name__)


# def add_review_tasks(scheduler: Scheduler):
#     connect(config.MONGO_DATABASE, host=config.MONGO_HOST, port=config.MONGO_PORT)
#     for info in ShopInfo.objects:
#         print(info)
#         scheduler.append_url(f'https://www.dianping.com/shop/{info.id}/review_all?queryType=sortType&queryVal=latest',
#                              'comment_first', f'https://www.dianping.com/shop/{info.id}')
def add_topic_search_tasks(scheduler: Scheduler):
    for index in range(50):
        url = ''
        reference_url = ''
        keyword = urllib.parse.quote(config.KEYWORD)
        if index == 0:
            url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic'
        else:
            url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic&page={index+1}'
            reference_url = f'https://s.weibo.com/topic?q={keyword}&pagetype=topic&topic=1&Refer=weibo_topic&page={index}'

        scheduler.append_url(url, '', reference_url)
    pass


def add_topic_detail_tasks(scheduler: Scheduler):
    connect(config.MONGO_DATABASE, host=config.MONGO_HOST, port=config.MONGO_PORT)
    urls = set()
    for topic in SinaTopic.objects:
        if topic.url:
            urls.add(topic.url)

    for url in urls:
        scheduler.append_url(url, '', '')


def export():
    export_shops_to_excel('./output/shops.xls')
    export_reviews_to_excel('./output/reviews.xls')
    pass


def main():
    scheduler = Scheduler()
    # scheduler.append_url('https://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F', 'list', '')

    # add_topic_search_tasks(scheduler)
    # add_topic_detail_tasks(scheduler)

    scheduler.start()
    scheduler.join()

    # export()


if __name__ == '__main__':
    main()
