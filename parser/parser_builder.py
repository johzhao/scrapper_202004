from typing import Optional
from urllib.parse import urlparse

from .parser import Parser
from .sina_weibo import search_list_parser
from .sina_weibo import topic_list_parser


def get_parser(url: str, delegate) -> Optional[Parser]:
    url_components = urlparse(url)
    if url_components.hostname == 's.weibo.com':
        if url_components.path == '/weibo' or url_components.path.startswith('/weibo/'):
            return search_list_parser.SearchListParser(delegate)
        elif url_components.path == '/topic':
            return topic_list_parser.TopicListParser(delegate)

    raise Exception(f'The is no supported parser for {url}')