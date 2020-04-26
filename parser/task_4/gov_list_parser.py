import datetime
import logging
import re
from typing import Optional

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

import config
from model.task import Task
from model.task_4_items import GovItem
from parser.parser import Parser
from parser.utility import get_element_str

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class GovListParser(Parser):
    publish_time_pattern = re.compile(r'(.*?)：(\d+).(\d+).(\d+)')

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//li[@class="res-list"]')
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

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[GovItem]:
        elements = html.xpath('h3/a')
        if not elements:
            raise Exception(f'Failed to parse item')

        element = elements[0]
        title = get_element_str(element)
        url = element.attrib['href']
        if not title:
            print('')

        abstract = ''
        abstract_elements = html.xpath('p[@class="res-sub"]')
        if abstract_elements:
            abstract = get_element_str(abstract_elements[0])

        try:
            element = html.xpath('.//p[@class="res-other"]/span')
            element = element[0]
            publish_str = element.text.strip()
            matches = self.publish_time_pattern.findall(publish_str)
            if not matches:
                raise Exception(f'Failed to parse publish datetime from {publish_str}')
            publish = datetime.datetime(int(matches[0][1]), int(matches[0][2]), int(matches[0][3]))
        except:
            return None

        item = GovItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element) -> Optional[Task]:
        element = html.xpath('//a[@id="snext"]')
        if not element:
            return None

        element = element[0]
        url = element.attrib['href']

        return Task(url, '', task.url, metadata=task.metadata)
