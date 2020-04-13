from os.path import normpath
from urllib.parse import urlparse, urlunparse


def parse_url():
    url = ('https://s.weibo.com/weibo?q=%23%E7%96%AB%E6%83%85%E5%8F%AF%E8%83%BD%E5%AF%BC%E8%87%B420%E4%B8%87%E7%BE%8E'
           '%E5%9B%BD%E4%BA%BA%E6%AD%BB%E4%BA%A1%23')
    url_components = urlparse(url)
    path = normpath(url_components.path)
    comment_url = urlunparse((url_components.scheme, url_components.netloc, path, url_components.params,
                              url_components.query, url_components.fragment))


if __name__ == '__main__':
    parse_url()
