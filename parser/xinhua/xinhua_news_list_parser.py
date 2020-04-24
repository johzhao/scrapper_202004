import datetime
import json
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

from model.xinhua_news_item import XinHuaNewsItem
from model.task import Task
from parser.parser import Parser
from parser.utility import get_element_str

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class XinHuaNewsListParser(Parser):

    def __init__(self, delegate):
        super().__init__(delegate)

    def parse(self, task: Task, content: str):
        data = json.loads(content)
        if data['code'] != 200:
            raise Exception(f'Failed to parse response {content}')

        content = data['content']
        keyword = content['keyword']
        news_items = content.get('results', [])

        need_next_page = False
        begin = datetime.datetime(2020, 1, 10)
        end = datetime.datetime(2020, 4, 11)

        items = []
        for news_item in news_items:
            item = XinHuaNewsItem()
            item.url = news_item['url']
            item.keyword = keyword
            item.title = news_item['title']
            item.abstract = news_item['des']
            item.publish = datetime.datetime.strptime(news_item['pubtime'], '%Y-%m-%d %H:%M:%S')
            item.created = datetime.datetime.now()
            items.append(item)
            if item.publish >= begin:
                need_next_page = True

        if need_next_page:
            params = task.params
            params['curPage'] += 1
            task = Task(task.url, '', '', params=params, metadata=task.metadata)
            self.delegate.append_request_task(task)

        # html = etree.HTML(content, etree.HTMLParser())
        # elements = html.xpath('//div[@class="newsList"]/div[@class="news"]')
        # if len(elements) == 0:
        #     raise Exception(f'Failed to parse item from {content}')

        # need_next_page = False
        # items = []
        # for element in elements:
        #     item = self._parse_search_item(element, task.metadata)
        #     if item:
        #         items.append(item)
        #         need_next_page = True
        #         # if item.publish >= begin:
        #         #     need_next_page = True
        #         #     if item.publish <= end:
        #         #         items.append(item)
        #
        # # Parse link for next page
        # if need_next_page:
        #     self._parse_next_page_request(task, html)

        for item in items:
            self.delegate.save_content(item, 'xinhua')

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[XinHuaNewsItem]:
        elements = html.xpath('h2/a')
        if not elements:
            raise Exception(f'Failed to parse item')

        element = elements[0]
        title = get_element_str(element)
        url = element.attrib['href']
        if not title:
            print('')

        abstract_elements = html.xpath('.//p[@class="newstext"]')
        # if not abstract_elements:
        #     return None

        abstract = get_element_str(abstract_elements[0])

        try:
            element = html.xpath('.//p[@class="newstime"]/span')
            element = element[0]
            publish_str = element.text.strip()
            publish = datetime.datetime.strptime(publish_str, '%y-%m-%d %H:%M:%S')
        except:
            return None

        item = XinHuaNewsItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, task: Task, html: _Element):
        element = html.xpath('//a[@id="snext"]')
        if not element:
            return

        element = element[0]
        url = element.attrib['href']

        # next_page_url = urljoin(task.url, url)
        # url_components = urlparse(next_page_url)
        # path = normpath(url_components.path)
        # next_page_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
        #                           url_components.query, url_components.fragment))
        self.delegate.append_request_task(Task(url, '', task.url, metadata=task.metadata))
