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

from model.china_cdc_item import ChinaCdcItem
from model.task import Task
from parser.parser import Parser
from parser.utility import get_element_str

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ChinaCdcListParser(Parser):
    publish_time_pattern = re.compile(r'(.*?)：(\d+)-(\d+)-(\d+)')

    def __init__(self, delegate):
        super().__init__(delegate)

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        titles = html.xpath('//div[@class="searchResult-con_news"]/p[@class="search-title-text"]/a')
        contents = html.xpath('//div[@class="searchResult-con_news"]/p[@class="search-con-text"]')
        publishs = html.xpath('//div[@class="searchResult-con_news"]/span[@class="search-contxt-time"]')

        if len(titles) == 0 or len(titles) != len(contents) or len(titles) != len(publishs):
            raise Exception(f'Failed to parse item from {content}')

        need_next_page = False
        begin = datetime.datetime(2020, 1, 10)
        end = datetime.datetime(2020, 4, 11)
        items = []
        count = len(titles)
        for index in range(count):
            item = self._parse_search_item(titles[index], contents[index], publishs[index], task.metadata)
            if item:
                items.append(item)
                if item.publish >= begin:
                    need_next_page = True

        # Parse link for next page
        if need_next_page:
            self._parse_next_page_request(task, html)

        for item in items:
            self.delegate.save_content(item, 'cnr')

    def _parse_search_item(self, html1: _Element, html2: _Element, html3: _Element, metadata: dict) -> Optional[ChinaCdcItem]:
        title = get_element_str(html1)
        url = html1.attrib['href']
        if not title:
            print('')

        abstract = get_element_str(html2)

        try:
            publish_str = html3.text.strip()
            matches = self.publish_time_pattern.findall(publish_str)
            if not matches:
                raise Exception(f'Failed to parse publish datetime from {publish_str}')
            publish = datetime.datetime(int(matches[0][1]), int(matches[0][2]), int(matches[0][3]))
        except:
            return None

        item = ChinaCdcItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element):
        element = html.xpath('//a[@class="next-page"]')
        if not element:
            return

        element = element[0]
        url = element.attrib['href']
        if not url.startswith('http'):
            url = urljoin(task.url, url)

        self.delegate.append_request_task(Task(url, '', task.url, metadata=task.metadata))
