import logging
import threading
import time

import config
from downloader.downloader import Downloader
from model.parsed_result_item import ParsedResultItem
from model.task import Task
from parser.parser_builder import get_parser
from scheduler.task_queue import TaskQueue

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

MAX_RETRY = 3


class Scheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.downloader = Downloader(config.HEADERS)
        self.task_queue = TaskQueue(config.REDIS_DB_URL, config.REDIS_DB_DATABASE)
        self.count = 0

    def append_request_task(self, task: Task):
        self.task_queue.push_task(task)
        # if self.count <= 50:
        #     self.task_queue.push_task(task)
        #     self.count += 1

    def run(self) -> None:
        retry = 0
        while True:
            task = self.task_queue.get_top_task()
            if task is None:
                break

            try:
                self._process_task(task)
                retry = 0
            except:
                if retry <= MAX_RETRY:
                    logger.warning(f'Failed to process task, attempt the {retry} retry.')
                    retry += 1
                    delay = retry * 10 + 10
                    time.sleep(delay)
                else:
                    raise

    def _process_task(self, task: Task) -> None:
        content = self.downloader.download_task(task)
        try:
            parser = get_parser(task.url)
            for item in parser.parse(task, content):
                if isinstance(item, Task):
                    self.task_queue.push_task(item)
                elif isinstance(item, ParsedResultItem):
                    logger.info(f'Save the parsed item {item}')
                    item.__class__.store_item(item)
                else:
                    raise Exception(f'Unsupported parse result: class={item.__class__}')

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
