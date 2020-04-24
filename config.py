HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/81.0.4044.92 Safari/537.36'),
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
               'application/signed-exchange;v=b3;q=0.9'),
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Referer': 'http://search1.china.com.cn/search/searchcn.jsp',
    'Origin': 'http://search1.china.com.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Upgrade-Insecure-Requests': '1',
}

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'cnr_items'


REDIS_DB_URL = 'redis://localhost:6379'
REDIS_DB_DATABASE = 0


DOWNLOAD_DELAY = 10

KEYWORD = '新冠'
# KEYWORD = '肺炎'
# KEYWORD = '武汉'
# KEYWORD = 'COVID-19'
# KEYWORD = '冠状病毒'
# KEYWORD = '疫情'
