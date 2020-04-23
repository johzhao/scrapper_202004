from typing import Optional
from urllib.parse import urlparse

from .china_news import china_news_list_parser
from .cnr import cnr_list_parser
from .gov import gov_list_parser
from .parser import Parser
from .people import people_list_parser
from .sina_news import sina_news_list_parser
from .sina_weibo import search_list_parser
from .sina_weibo import topic_list_parser
from .xinhua import xinhua_news_list_parser
from .china_cdc import china_cdc_list_parser
from .china import china_list_parser
from .cctv import cctv_list_parser
from .the_paper import the_paper_list_parser


def get_parser(url: str, delegate) -> Optional[Parser]:
    url_components = urlparse(url)
    if url_components.hostname == 's.weibo.com':
        if url_components.path == '/weibo' or url_components.path.startswith('/weibo/'):
            return search_list_parser.SearchListParser(delegate)
        elif url_components.path == '/topic':
            return topic_list_parser.TopicListParser(delegate)
    elif url_components.hostname == 'was.cnr.cn':
        return cnr_list_parser.CnrListParser(delegate)
    elif url_components.hostname == 'so.news.cn':
        return xinhua_news_list_parser.XinHuaNewsListParser(delegate)
    elif url_components.hostname == 'search.people.com.cn':
        return people_list_parser.PeopleListParser(delegate)
    elif url_components.hostname == 'sou.chinanews.com':
        return china_news_list_parser.ChinaNewsListParser(delegate)
    elif url_components.hostname == 'search.sina.com.cn':
        return sina_news_list_parser.SinaNewsListParser(delegate)
    elif url_components.hostname == 'sousuo.gov.cn':
        return gov_list_parser.GovListParser(delegate)
    elif url_components.hostname == 'www.chinacdc.cn':
        return china_cdc_list_parser.ChinaCdcListParser(delegate)
    elif url_components.hostname == 'search1.china.com.cn':
        return china_list_parser.ChinaListParser(delegate)
    elif url_components.hostname == 'search.cctv.com':
        return cctv_list_parser.CCTVListParser(delegate)
    elif url_components.hostname == 'www.thepaper.cn':
        return the_paper_list_parser.ThePaperListParser(delegate)

    raise Exception(f'The is no supported parser for {url}')
