from typing import Optional
from urllib.parse import urlparse

from .parser import Parser
from .sina_weibo import search_list_parser
from .sina_weibo import topic_list_parser
from .task_4 import cctv_list_parser, china_list_parser, china_cdc_list_parser, china_news_list_parser, cnr_list_parser, \
    gov_list_parser, people_list_parser, sina_news_list_parser, xinhua_news_list_parser


def get_parser(url: str) -> Optional[Parser]:
    url_components = urlparse(url)
    if url_components.hostname == 's.weibo.com':
        if url_components.path == '/weibo' or url_components.path.startswith('/weibo/'):
            return search_list_parser.SearchListParser()
        elif url_components.path == '/topic':
            return topic_list_parser.TopicListParser()
    elif url_components.hostname == 'was.cnr.cn':
        return cnr_list_parser.CnrListParser()
    elif url_components.hostname == 'so.news.cn':
        return xinhua_news_list_parser.XinHuaNewsListParser()
    elif url_components.hostname == 'search.people.com.cn':
        return people_list_parser.PeopleListParser()
    elif url_components.hostname == 'sou.chinanews.com':
        return china_news_list_parser.ChinaNewsListParser()
    elif url_components.hostname == 'search.sina.com.cn':
        return sina_news_list_parser.SinaNewsListParser()
    elif url_components.hostname == 'sousuo.gov.cn':
        return gov_list_parser.GovListParser()
    elif url_components.hostname == 'www.chinacdc.cn':
        return china_cdc_list_parser.ChinaCdcListParser()
    elif url_components.hostname == 'search1.china.com.cn':
        return china_list_parser.ChinaListParser()
    elif url_components.hostname == 'search.cctv.com':
        return cctv_list_parser.CCTVListParser()

    raise Exception(f'The is no supported parser for {url}')
