import datetime
import json
import logging

import config
from model.task import Task
from model.task_4_items import XinHuaNewsItem
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class XinHuaNewsListParser(Parser):

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        data = json.loads(content)
        if data['code'] != 200:
            raise Exception(f'Failed to parse response {content}')

        content = data['content']
        keyword = content['keyword']
        news_items = content.get('results', [])

        need_next_page = False
        items = []
        for news_item in news_items:
            item = XinHuaNewsItem()
            item.url = news_item['url']
            item.keyword = keyword
            item.title = news_item['title']
            item.abstract = news_item['des']
            item.publish = datetime.datetime.strptime(news_item['pubtime'], '%Y-%m-%d %H:%M:%S')
            items.append(item)
            if item.publish >= config.BEGIN_DATE:
                need_next_page = True

        if need_next_page:
            params = task.params
            params['curPage'] += 1
            yield Task(task.url, '', '', params=params, metadata=task.metadata)

        for item in items:
            yield item
