import datetime
import logging
import re
from typing import Optional
from urllib.parse import urljoin

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element
from model.task_4_items import CctvItem

from model.task import Task
from parser.parser import Parser
from parser.utility import get_element_str
import config

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CCTVListParser(Parser):
    publish_time_pattern = re.compile(r'发布时间：(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')
    next_page_pattern = re.compile(r'javascript:gopage\((\d+)\)')

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[@class="outer"]/ul/li')
        if len(elements) == 0:
            raise Exception(f'Failed to parse item from {content}')

        need_next_page = False
        items = []
        for element in elements:
            item = self._parse_search_item(element, task.metadata)
            if item:
                items.append(item)
                if item.publish >= config.BEGIN_DATE:
                    need_next_page = True

        # Parse link for next page
        if need_next_page:
            new_task = self._parse_next_page_request(task, html)
            if new_task:
                yield new_task

        for item in items:
            yield item

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[CctvItem]:
        elements = html.xpath('.//h3/span/a')
        if not elements:
            raise Exception(f'Failed to parse item')

        element = elements[0]
        title = get_element_str(element)
        url = element.attrib['href']

        abstract_elements = html.xpath('.//p[@class="bre"]')
        abstract = get_element_str(abstract_elements[0])

        try:
            element = html.xpath('.//span[@class="tim"]')
            element = element[0]
            publish_str = element.text.strip()
            matches = self.publish_time_pattern.findall(publish_str)
            if not matches:
                raise Exception(f'Failed to parse publish datetime from {publish_str}')

            publish = datetime.datetime(int(matches[0][0]), int(matches[0][1]), int(matches[0][2]),
                                        int(matches[0][3]), int(matches[0][4]), int(matches[0][5]))
        except:
            return None

        item = CctvItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    @staticmethod
    def _parse_next_page_request(task: Task, html: _Element) -> Optional[Task]:
        element = html.xpath('//a[@class="page-next"]')
        if not element:
            return None

        element = element[0]
        if element.text == '下一页':
            url = element.attrib['href']
            next_page_url = urljoin(task.url, url)

            return Task(next_page_url, '', task.url, metadata=task.metadata)

        return None
