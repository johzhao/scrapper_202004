import datetime
import logging
import re
from posixpath import normpath
from typing import Optional
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from model.china_item import ChinaItem
from model.task import Task
from parser.parser import Parser
from parser.utility import get_element_str

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ChinaListParser(Parser):
    publish_time_pattern = re.compile(r'(.*?)\s+(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')
    next_page_pattern = re.compile(r'javascript:gopage\((\d+)\)')

    def __init__(self, delegate):
        super().__init__(delegate)

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//table[3]//tr')
        if len(elements) == 0:
            raise Exception(f'Failed to parse item from {content}')

        need_next_page = False
        begin = datetime.datetime(2020, 1, 10)
        end = datetime.datetime(2020, 4, 11)
        items = []
        index = 0
        count = len(elements)
        while index < count:
            item = self._parse_search_item(elements[index+1], elements[index+2], elements[index+3], task.metadata)
            if item:
                items.append(item)
                if item.publish >= begin:
                    need_next_page = True
            index += 4

        # Parse link for next page
        if need_next_page:
            self._parse_next_page_request(task, html)

        for item in items:
            self.delegate.save_content(item, 'china')

    def _parse_search_item(self, html1: _Element, html2: _Element, html3: _Element, metadata: dict) -> Optional[ChinaItem]:
        elements = html1.xpath('./td/a')
        if not elements:
            raise Exception(f'Failed to parse item')

        element = elements[0]
        title = get_element_str(element)
        url = element.attrib['href']

        abstract_elements = html2.xpath('./td/a')
        abstract = get_element_str(abstract_elements[0])

        try:
            element = html3.xpath('./td/a[2]/font')
            element = element[0]
            publish_str = element.text.strip()
            publish = datetime.datetime.strptime(publish_str, '%Y-%m-%d')
        except:
            return None

        item = ChinaItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element):
        element = html.xpath('//form[@id="page_form"]//a')
        if not element:
            return

        element = element[-1]
        if element.text == '[下一页]':
            url = element.attrib['href']

            matchs = self.next_page_pattern.findall(url)
            if not matchs:
                return
            value = int(matchs[0])

            body = task.body
            if 'page' in body:
                body['page'] += 1
            else:
                body['page'] = value

            self.delegate.append_request_task(Task(task.url, '', task.url, method='POST',
                                                   body=body, metadata=task.metadata))
