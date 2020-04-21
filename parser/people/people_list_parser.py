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

from model.people_item import PeopleItem
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PeopleListParser(Parser):

    def __init__(self, delegate):
        super().__init__(delegate)

    def parse(self, url: str, content: str, metadata: dict):
        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//div[contains(@class, "fr")]/ul')
        if len(elements) == 0:
            raise Exception(f'Failed to parse item from {content}')

        need_next_page = False
        begin = datetime.datetime(2020, 1, 10)
        end = datetime.datetime(2020, 4, 11)
        items = []
        for element in elements:
            item = self._parse_search_item(element, metadata)
            if item:
                items.append(item)
                need_next_page = True
                # if item.publish >= begin:
                #     need_next_page = True
                #     if item.publish <= end:
                #         items.append(item)

        # Parse link for next page
        if need_next_page:
            self._parse_next_page_request(url, html, metadata)

        for item in items:
            self.delegate.save_content(item, 'cnr')

    def _parse_search_item(self, html: _Element, metadata: dict) -> Optional[PeopleItem]:
        element = html.xpath('li/b/a')[0]
        title = element.text
        url = element.attrib['href']

        abstract = html.xpath('li[2]')[0].text

        try:
            element = html.xpath('li[3]/a')
            element = element[0]
            publish_str = element.tail.strip()
            publish = datetime.datetime.strptime(publish_str, '%Y-%m-%d %H:%M:%S')
        except:
            return None

        item = PeopleItem()
        item.title = title
        item.url = url
        item.keyword = metadata.get('keyword', '')
        item.abstract = abstract
        item.publish = publish

        return item

    def _parse_next_page_request(self, reference: str, html: _Element, metadata: dict):
        element = html.xpath('//div[@class="show_nav_bar"]/a')
        if not element:
            return

        element = element[-1]
        if element.text == '下一页':
            url = element.attrib['href']

            comment_url = urljoin(reference, url)
            url_components = urlparse(comment_url)
            path = normpath(url_components.path)
            comment_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
                                      url_components.query, url_components.fragment))
            self.delegate.append_url(comment_url, '', reference, metadata)
