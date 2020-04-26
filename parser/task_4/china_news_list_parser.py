import datetime
import logging
import re
from typing import Optional

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

import config
from model.task_4_items import ChinaNewsItem
from model.task import Task
from parser import utility
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ChinaNewsListParser(Parser):
    start_value_pattern = re.compile(r'javascript:ongetkey\((\d+)\)')

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[@id="news_list"]/table')
        if len(elements) == 0:
            raise Exception(f'Failed to parse item from {content}')

        need_next_page = False
        items = []
        for element in elements:
            item = self._parse_search_item(element, task.metadata)
            if item.publish >= config.BEGIN_DATE:
                need_next_page = True

        # Parse link for next page
        if need_next_page:
            new_task = self._parse_next_page_request(task, html)
            if new_task:
                yield new_task

        for item in items:
            yield item

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[ChinaNewsItem]:
        element = html.xpath('.//li[contains(@class, "news_title")]/a')[0]
        title = utility.get_element_str(element)
        url = element.attrib['href']

        abstract = utility.get_element_str(html.xpath('.//li[@class="news_content"]')[0])

        try:
            element = html.xpath('.//li[@class="news_other"]')
            element = element[0]
            publish_str = element.text.strip()
            publish_str = publish_str.split('\t')[-1]
            publish = datetime.datetime.strptime(publish_str, '%Y-%m-%d %H:%M:%S')
        except:
            return None

        item = ChinaNewsItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element) -> Optional[Task]:
        elements = html.xpath('//div[@id="pagediv"]/a')
        if not elements:
            return None

        for element in elements:
            if element.text == '下一页':
                href = element.attrib['href']
                matches = self.start_value_pattern.findall(href)
                if not matches:
                    raise Exception(f'Failed to find value from {href}')

                value = int(matches[0])
                new_body = task.body
                new_body['start'] = value * 10
                return Task(task.url, task.type_, task.url, method='POST', body=new_body, metadata=task.metadata)
