import logging
import re
from datetime import datetime

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from config import KEYWORD
from model.sina_topic import SinaTopic
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TopicListParser(Parser):
    read_comment_count_pattern = re.compile(r'(.+)?讨论\s(.+)?阅读')

    def __init__(self):
        super().__init__()

    def parse(self, url: str, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[contains(@class, "card")]/div[@class="info"]')
        if len(elements) == 0:
            raise Exception(f'Failed to parse comments from {content}')

        items = []
        for element in elements:
            name, url = self._parse_topic_name_and_url(element)
            read_count, comment_count = self._parse_read_and_comment_count(element)

            item = SinaTopic()
            item.keyword = KEYWORD
            item.topic = name
            item.url = url
            item.read_count = read_count
            item.comment_count = comment_count
            item.created = datetime.now()

            items.append(item)

        for item in items:
            yield item

    def _parse_topic_name_and_url(self, html: _Element) -> (str, str):
        elements = html.xpath('div/a[@class="name"]')
        if not elements:
            raise Exception('Failed to find topic name.')
        name = elements[0].text
        url = elements[0].attrib['href']
        return name, url

    def _parse_read_and_comment_count(self, html: _Element) -> (str, str):
        elements = html.xpath('p')
        if not elements:
            raise Exception('Failed to find topic name.')

        data = elements[-1].text
        matchs = self.read_comment_count_pattern.findall(data)
        if not matchs:
            raise Exception('Failed to parse the read and comment count')

        return matchs[0][0], matchs[0][1]
