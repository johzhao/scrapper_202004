import logging

import config
from downloader.downloader import Downloader
from model.task import Task

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_downloader():
    downloader = Downloader(config.HEADERS)
    task = Task('https://www.dianping.com/shop/90556783/review_all', '', 'https://www.dianping.com/shop/90556783')
    result = downloader.download_task(task)
    logger.info(result)
