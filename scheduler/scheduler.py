import logging
import threading
import time

from mongoengine import Document

import config
from downloader.downloader import Downloader
from model.task import Task
from parser.parser_builder import get_parser
from scheduler.task_queue import TaskQueue
from storage.storage import Storage

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Scheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.downloader = Downloader(config.HEADERS)
        self.storage = Storage(config.MONGO_DATABASE, config.MONGO_HOST, config.MONGO_PORT)
        self.task_queue = TaskQueue(config.REDIS_DB_URL, config.REDIS_DB_DATABASE)
        self.count = 0

    def save_content(self, content: Document, type_: str):
        self.storage.save_content(content, type_)

    def append_request_task(self, task: Task):
        self.task_queue.push_task(task)
        # if self.count <= 50:
        #     self.task_queue.push_task(task)
        #     self.count += 1

    def run(self) -> None:
        while True:
            task = self.task_queue.get_top_task()
            if task is None:
                break

            content = self.downloader.download_url(task)
            try:
                parser = get_parser(task.url, self)
                parser.parse(task, content)
            except Exception as e:
                with open('exception.html', 'w') as ofile:
                    ofile.write(content)
                logger.error(f'Parse failed with error:')
                logger.exception(e)
                raise

            self.task_queue.drop_top_task(task.type_)

            # 等待指定的秒数+-2s
            # delay = config.DOWNLOAD_DELAY + random.randint(20, 50) / 10
            delay = config.DOWNLOAD_DELAY
            logger.info(f'Delay for {delay} seconds.')
            time.sleep(delay)
