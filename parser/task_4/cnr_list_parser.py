import datetime
import logging
from posixpath import normpath
from typing import Optional
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlunparse

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from model.task_4_items import CnrItem

import config
from model.task import Task
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CnrListParser(Parser):

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//td[@class="searchresult"]/ol/li')
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

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[CnrItem]:
        element = html.xpath('div[1]/a')[0]
        title = element.text
        url = element.attrib['href']

        try:
            element = html.xpath('div/span[@class="searchresulturl"]')
            element = element[0]
            publish_str = element.tail.strip()
            publish = datetime.datetime.strptime(publish_str, '%Y.%m.%d %H:%M:%S')
        except:
            return None

        item = CnrItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element) -> Optional[Task]:
        element = html.xpath('//a[@class="next-page"]')
        if not element:
            return None

        element = element[0]
        url = element.attrib['href']

        comment_url = urljoin(task.url, url)
        url_components = urlparse(comment_url)
        path = normpath(url_components.path)
        comment_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
                                  url_components.query, url_components.fragment))
        return Task(comment_url, '', task.url, metadata=task.metadata)
