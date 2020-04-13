import logging
import re
from datetime import datetime

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from model.sina_weibo import SinaWeibo
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SearchListParser(Parser):
    publish_time_pattern_1 = re.compile(r'(\d+)月(\d+)日\s+(\d+):(\d+)')
    publish_time_pattern_2 = re.compile(r'今天(\d+):(\d+)')
    forward_pattern = re.compile(r'转发\s*(\d*)')
    comment_pattern = re.compile(r'评论\s*(\d*)')

    def __init__(self, delegate):
        super().__init__(delegate)

    def parse(self, url: str, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[@class="card-wrap"]/div[@class="card"]')
        if len(elements) == 0:
            raise Exception(f'Failed to parse comments from {content}')

        reviews = []
        for element in elements:
            content_element = element.xpath('div[@class="card-feed"]/div[@class="content"]')[0]
            username = self._parse_username(content_element)
            content = self._parse_content(content_element)
            publish_time = self._parse_publish_time(content_element)

            action_elements = element.xpath('div[@class="card-act"]/ul/li')
            forward_count = self._parse_forward_count(action_elements[1])
            comment_count = self._parse_comment_count(action_elements[2])
            favor_count = self._parse_favor_count(action_elements[3])

            item = SinaWeibo()
            # TODO: Set the keyword
            item.url = url
            item.username = username
            item.content = content
            item.publish = publish_time
            item.forward_count = forward_count
            item.comment_count = comment_count
            item.favor_count = favor_count
            item.created = datetime.now()
            logger.info(item)

            self.delegate.save_content(item, 'weibo')

        raise Exception('Not implement')

    def _parse_username(self, html: _Element) -> str:
        element = html.xpath('div[@class="info"]//a[@class="name"]')
        return element[0].text

    def _parse_content(self, html: _Element) -> str:
        pass

    def _parse_publish_time(self, html: _Element) -> datetime:
        element = html.xpath('p[@class="from"]/a')
        publish_time_str = element[0].text.strip()

        publish_matchs = self.publish_time_pattern_1.findall(publish_time_str)
        if len(publish_matchs) == 1:
            return datetime(2020, int(publish_matchs[0][0]), int(publish_matchs[0][1]), int(publish_matchs[0][2]),
                            int(publish_matchs[0][3]))

        publish_matchs = self.publish_time_pattern_2.findall(publish_time_str)
        if len(publish_matchs) == 1:
            publish_time = datetime.now()
            publish_time.replace(hour=int(publish_matchs[0][0]), minute=int(publish_matchs[0][1]))
            return publish_time

        raise Exception(f'Failed to parse publish time {publish_time_str}')

    def _parse_forward_count(self, html: _Element) -> int:
        element = html.xpath('a')[0]
        forward_str = element.text.strip()
        if forward_str == '转发':
            return 0
        else:
            matchs = self.forward_pattern.findall(forward_str)
            if len(matchs) != 1:
                raise Exception(f'Failed to parse forward count {forward_str}')
            forward = int(matchs[0])
            return forward

    def _parse_comment_count(self, html: _Element) -> int:
        element = html.xpath('a')[0]
        comment_str = element.text.strip()
        if comment_str == '评论':
            return 0
        else:
            matchs = self.comment_pattern.findall(comment_str)
            if len(matchs) != 1:
                raise Exception(f'Failed to parse comment count {comment_str}')
            comment = int(matchs[0])
            return comment

    def _parse_favor_count(self, html: _Element) -> int:
        element = html.xpath('a/em')[0]
        if not element.text:
            return 0
        else:
            return int(element.text.strip())
