import logging
import re
from typing import Optional
from urllib.parse import urlparse, urlunparse

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from model.sina_topic_v2 import WeiboTopicItem
from model.task import Task
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TopicListParser(Parser):
    next_page_href_pattern = re.compile(r'page=(\d+)')

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[contains(@class, "card")]/div[@class="info"]')
        if len(elements) == 0:
            raise Exception(f'Failed to parse comments from {content}')

        items = []
        for element in elements:
            name, _ = self._parse_topic_name_and_url(element)

            item = WeiboTopicItem()
            item.keyword = task.metadata['keyword']
            item.title = name

            items.append(item)

        new_task = self._parse_next_task(task, html)
        if new_task:
            yield new_task

        for item in items:
            yield item

    def _parse_topic_name_and_url(self, html: _Element) -> (str, str):
        elements = html.xpath('div/a[@class="name"]')
        if not elements:
            raise Exception('Failed to find topic name.')
        name = elements[0].text
        url = elements[0].attrib['href']
        return name, url

    def _parse_next_task(self, task: Task, html: _Element) -> Optional[Task]:
        elements = html.xpath('//a[@class="next"]')
        if not elements:
            return None

        url = elements[0].attrib['href']
        next_page_url_components = urlparse(url)
        query = next_page_url_components.query
        matches = self.next_page_href_pattern.findall(query)
        if not matches:
            return None

        page_num = int(matches[0])
        if page_num > 50:
            return None

        task_url_components = urlparse(task.url)
        new_task_url = urlunparse((task_url_components.scheme, task_url_components.netloc, task_url_components.path,
                                   task_url_components.params, next_page_url_components.query,
                                   task_url_components.fragment))
        return Task(new_task_url, '', task.url, metadata=task.metadata)
