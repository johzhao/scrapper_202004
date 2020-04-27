import logging
import re
import datetime

from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

from model.sina_weibo import SinaWeibo
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SearchListParser(Parser):
    title_pattern = re.compile(r'【(.+)?】')
    publish_time_pattern_1 = re.compile(r'(\d+)月(\d+)日\s+(\d+):(\d+)')
    publish_time_pattern_2 = re.compile(r'今天\s*?(\d+):(\d+)')
    publish_time_pattern_3 = re.compile(r'(\d+)?分钟前')
    publish_time_pattern_4 = re.compile(r'(\d+)-(\d+)-(\d+)\s+(\d+):(\d+)')
    forward_pattern = re.compile(r'转发\s*(\d*)')
    comment_pattern = re.compile(r'评论\s*(\d*)')

    def __init__(self):
        super().__init__()

    def parse(self, url: str, content: str):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[@class="card-wrap"]/div[@class="card"]')
        if len(elements) == 0:
            raise Exception(f'Failed to parse comments from {content}')

        items = []
        for element in elements:
            content_element = element.xpath('div[@class="card-feed"]/div[@class="content"]')[0]
            username = self._parse_username(content_element)
            content = self._parse_content(content_element)
            publish_time = self._parse_publish_time(content_element)

            title = ''
            title_match = self.title_pattern.findall(content)
            if title_match:
                title = title_match[0]

            action_elements = element.xpath('div[@class="card-act"]/ul/li')
            forward_count = self._parse_forward_count(action_elements[1])
            comment_count = self._parse_comment_count(action_elements[2])
            favor_count = self._parse_favor_count(action_elements[3])

            item = SinaWeibo()
            item.keyword = KEYWORD
            item.url = url
            item.username = username
            item.title = title
            item.content = content
            item.publish = publish_time
            item.forward_count = forward_count
            item.comment_count = comment_count
            item.favor_count = favor_count
            item.created = datetime.datetime.now()
            items.append(item)

        for item in items:
            yield item

    def _parse_username(self, html: _Element) -> str:
        elements = html.xpath('div[@class="info"]//a[@class="name"]')
        return elements[0].text

    def _parse_content(self, html: _Element) -> str:
        element = html.xpath('p[@class="txt"]')[-1]

        content = []
        if element.text is not None:
            content.append(element.text.strip())

        for child in element.getchildren():
            if child.tag == 'em':
                content.append(child.text.strip())
            elif child.tag == 'a':
                if child.text is not None:
                    content.append(child.text.strip())

                for sub_child in child.getchildren():
                    if sub_child.tag == 'i':
                        continue

                    if sub_child.text:
                        content.append(sub_child.text.strip())

                    if sub_child.tail is not None:
                        content.append(sub_child.tail.strip())

            elif child.text is not None:
                content.append(child.text.strip())

            if child.tail is not None:
                content.append(child.tail.strip())

        return ''.join(content)

    def _parse_publish_time(self, html: _Element) -> datetime:
        elements = html.xpath('p[@class="from"]/a')

        publish_time_str = ''
        for element in elements:
            publish_time_str = element.text.strip()

            publish_matchs = self.publish_time_pattern_1.findall(publish_time_str)
            if len(publish_matchs) == 1:
                return datetime.datetime(2020, int(publish_matchs[0][0]), int(publish_matchs[0][1]),
                                         int(publish_matchs[0][2]), int(publish_matchs[0][3]))

            publish_matchs = self.publish_time_pattern_4.findall(publish_time_str)
            if len(publish_matchs) == 1:
                return datetime.datetime(int(publish_matchs[0][0]), int(publish_matchs[0][1]),
                                         int(publish_matchs[0][2]), int(publish_matchs[0][3]),
                                         int(publish_matchs[0][4]))

            publish_matchs = self.publish_time_pattern_2.findall(publish_time_str)
            if len(publish_matchs) == 1:
                publish_time = datetime.datetime.now()
                publish_time.replace(hour=int(publish_matchs[0][0]), minute=int(publish_matchs[0][1]))
                return publish_time

            publish_matchs = self.publish_time_pattern_3.findall(publish_time_str)
            if len(publish_matchs) == 1:
                publish_time = datetime.datetime.now()
                minutes = int(publish_matchs[0])
                publish_time -= datetime.timedelta(minutes=minutes)
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
