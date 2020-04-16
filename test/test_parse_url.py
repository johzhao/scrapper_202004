import datetime
from os.path import normpath
from urllib.parse import urlparse, urlunparse, unquote


def parse_url():
    url = ('https://s.weibo.com/weibo?q=%23%E7%96%AB%E6%83%85%E5%8F%AF%E8%83%BD%E5%AF%BC%E8%87%B420%E4%B8%87%E7%BE%8E'
           '%E5%9B%BD%E4%BA%BA%E6%AD%BB%E4%BA%A1%23')
    url_components = urlparse(url)
    path = normpath(url_components.path)
    comment_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
                              url_components.query, url_components.fragment))


def parse_url_v2():
    url = ('https://s.weibo.com/weibo?q=%23%E5%93%80%E6%82%BC%E6%8A%97%E5%87%BB%E6%96%B0%E5%86%A0%E7%96%AB%E6%83%85%E7'
           '%89%BA%E7%89%B2%E7%83%88%E5%A3%AB%E5%92%8C%E9%80%9D%E4%B8%96%E5%90%8C%E8%83%9E%23&page=9')
    url_components = urlparse(url)
    queries = url_components.query.split('&')
    for query in queries:
        if not query.startswith('q='):
            continue
        fields = query.split('=')
        if len(fields) != 2:
            break
        topic = fields[1]
        topic = unquote(topic)
        break
    print('')


def parse_url_v3():
    url = 'https://s.weibo.com/weibo/%23%E4%BB%80%E4%B9%88%E6%98%AF%E6%AD%A6%E6%B1%89%23'
    url_components = urlparse(url)
    fields = url_components.path.split('/')
    topic = unquote(fields[-1])
    print('')


if __name__ == '__main__':
    # parse_url()
    # parse_url_v2()
    # parse_url_v3()
    now = datetime.datetime.now()
    s = now.strftime('%Y-%m-%d %H:%M:%S')
    print(s)
