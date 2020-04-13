import json
import logging
import os
import re
from typing import Optional

import requests
from lxml import etree
# noinspection PyProtectedMember
from lxml.etree import _Element

import config
from parser.dianping.font_parser import FontParser
from parser.dianping.shop_detail_css_parser import ShopDetailCSSParser
from parser.parser import Parser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class DetailParser(Parser):
    font_parser = FontParser()
    css_parser = ShopDetailCSSParser()
    css_pattern = re.compile(r'(//s3plus.meituan.net/v1/.+?/svgtextcss/.+?\.css)')
    review_count_pattern = re.compile(r'(\d+?)\s*?条评论')
    avg_cost_pattern = re.compile(r'消费:\s*?(\d+?)\s*?元')
    prod_rating_pattern = re.compile(r'产品:\s*?([.0-9]+)')
    env_rating_pattern = re.compile(r'环境:\s*?([.0-9]+)')
    service_rating_pattern = re.compile(r'服务:\s*?([.0-9]+)')
    phone_number_pattern = re.compile(r'电话：\s*?(.*)')

    def __init__(self, delegate):
        super().__init__(delegate)
        self.font_parser.setup_base_font_mapping('./test_files/basefont.woff', './test_files/basefont.json', 'address')
        self.font_parser.setup_base_font_mapping('./test_files/basefont_v1.woff', './test_files/basefont_v1.json',
                                                 'num')

    def parse(self, url: str, content: str):
        html = etree.HTML(content, etree.HTMLParser())

        info = html.xpath('//div[@id="basic-info"]')
        if len(info) == 0:
            raise Exception(f'Failed to parse shop info')

        css_url = self._parse_css(content)
        num_font_url = self.css_parser.get_font_url_by_type(css_url, 'num')
        address_font_url = self.css_parser.get_font_url_by_type(css_url, 'address')

        self.font_parser.append_font('num', num_font_url)
        self.font_parser.append_font('address', address_font_url)

        _, shop_id = os.path.split(url)

        shop_info = ShopInfo()
        shop_info.id = shop_id
        shop_info.name = self._parse_shop_name(html)
        shop_info.address = self._parse_address(html, num_font_url, address_font_url)
        shop_info.phone_number = self._parse_phone_number(shop_id, html, num_font_url)
        shop_info.url = url
        shop_info.rating = self._parse_shop_rating(html)
        shop_info.reviews = self._parse_review_count(html, num_font_url)
        shop_info.avg_cost = self._parse_avg_cost(html, num_font_url)
        shop_info.production_rating = self._parse_prod_rating(html, num_font_url)
        shop_info.environment_rating = self._parse_env_rating(html, num_font_url)
        shop_info.service_rating = self._parse_service_rating(html, num_font_url)

        self.delegate.save_content(shop_info, 'detail')

        # element = html.xpath('//p[@class="comment-all"]/a/@href')
        # comment_url = urljoin(url, element[0])
        # url_components = urlparse(comment_url)
        # path = normpath(url_components.path)
        # comment_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
        #                           url_components.query, url_components.fragment))
        # self.delegate.append_url(comment_url, 'comment', url)

    def _parse_css(self, content: str) -> str:
        css_matchs = self.css_pattern.findall(content)
        if len(css_matchs) != 1:
            raise Exception(f'Find {len(css_matchs)} css in the content')

        return f'http:{css_matchs[0]}'

    @staticmethod
    def _parse_shop_name(html: _Element) -> str:
        elements = html.xpath('//h1[@class="shop-name"]/text()')
        return ''.join(elements).strip()

    @staticmethod
    def _parse_shop_rating(html: _Element) -> str:
        elements = html.xpath('//span[contains(@class, "mid-rank-stars")]/@title')
        return elements[0].strip()

    def _parse_review_count(self, html: _Element, num_font_url: str) -> int:
        elements = html.xpath('//span[@id="reviewCount"]')
        content = self._parse_number(elements[0], num_font_url)
        matches = self.review_count_pattern.findall(content)
        if len(matches) != 1:
            raise Exception(f'Not found review count from {content}')
        return int(matches[0])

    def _parse_avg_cost(self, html: _Element, num_font_url: str) -> Optional[float]:
        elements = html.xpath('//span[@id="avgPriceTitle"]')
        content = self._parse_number(elements[0], num_font_url)
        matches = self.avg_cost_pattern.findall(content)
        if len(matches) != 1:
            logger.warning(f'Not found production rating from {content}')
            return None
        return float(matches[0])

    def _parse_prod_rating(self, html: _Element, num_font_url: str) -> Optional[float]:
        elements = html.xpath('//span[@id="comment_score"]/span[1]')
        content = self._parse_number(elements[0], num_font_url)
        matches = self.prod_rating_pattern.findall(content)
        if len(matches) != 1:
            logger.warning(f'Not found production rating from {content}')
            return None
        return float(matches[0])

    def _parse_env_rating(self, html: _Element, num_font_url: str) -> Optional[float]:
        elements = html.xpath('//span[@id="comment_score"]/span[2]')
        content = self._parse_number(elements[0], num_font_url)
        matches = self.env_rating_pattern.findall(content)
        if len(matches) != 1:
            logger.warning(f'Not found environment rating from {content}')
            return None
        return float(matches[0])

    def _parse_service_rating(self, html: _Element, num_font_url: str) -> Optional[float]:
        elements = html.xpath('//span[@id="comment_score"]/span[3]')
        content = self._parse_number(elements[0], num_font_url)
        matches = self.service_rating_pattern.findall(content)
        if len(matches) != 1:
            logger.warning(f'Not found service rating from {content}')
            return None
        return float(matches[0])

    def _parse_address(self, html: _Element, num_font_url: str, address_font_url: str) -> str:
        element = html.xpath('//span[@id="address"]')[0]

        result = []
        if element.text is not None:
            result.append(element.text.strip())

        for child in element.iterchildren():
            if child.attrib['class'] == 'address':
                result.append(self.font_parser.parse('address', address_font_url, child.text).strip())
            elif child.attrib['class'] == 'num':
                result.append(self.font_parser.parse('num', num_font_url, child.text).strip())
            else:
                result.append(child.text.strip())

            if child.tail is not None:
                result.append(child.tail.strip())

        return ''.join(result).strip()

    def _parse_phone_number(self, shop_id: str, html: _Element, num_font_url: str) -> str:
        url = f'http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId={shop_id}'
        logger.info(f'Request for {url}')
        response = requests.get(url, headers=config.HEADERS)

        try:
            data = json.loads(response.text)
        except Exception:
            logger.error(f'Failed to load data as json {response.text}')
            raise

        content = data['msg']['shopInfo']['phoneNo']
        if not content:
            return None

        html = etree.HTML(content, etree.HTMLParser())
        elements = html.xpath('//body')
        content = self._parse_number(elements[0], num_font_url)
        return content

    def _parse_number(self, element: _Element, num_font_url: str) -> str:
        result = []
        if element.text is not None:
            result.append(element.text.strip())

        for child in element.iterchildren():
            if child.tag == 'p':
                result.append(self._parse_number(child, num_font_url))
            elif child.attrib['class'] == 'num':
                result.append(self.font_parser.parse('num', num_font_url, child.text).strip())
            else:
                result.append(child.text.strip())

            if child.tail is not None:
                result.append(child.tail.strip())

        return ''.join(result).strip()
