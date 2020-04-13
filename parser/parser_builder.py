from typing import Optional
from urllib.parse import urlparse

from .parser import Parser
from .sina_weibo import search_list_parser


def get_parser(url: str, delegate) -> Optional[Parser]:
    url_components = urlparse(url)
    if url_components.hostname == 's.weibo.com' and url_components.path == '/weibo':
        return search_list_parser.SearchListParser(delegate)

    raise Exception(f'The is no supported parser for {url}')
