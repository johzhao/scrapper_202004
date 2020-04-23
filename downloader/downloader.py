import logging
from urllib.parse import urlparse

import requests

from model.task import Task

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Downloader:

    def __init__(self, headers: dict):
        self.session = requests.session()
        self.session.headers.update(headers)

    def download_url(self, task: Task) -> str:
        logger.info((f'Prepare to download the url {task.url} with the reference {task.reference}, '
                     f'params {task.params}'))

        url_components = urlparse(task.url)
        self.session.headers['host'] = url_components.hostname

        if task.reference:
            self.session.headers['Referer'] = task.reference
        else:
            self.session.headers.pop('Referer', None)

        if task.method == 'GET':
            if task.params:
                response = self.session.get(task.url, params=task.params)
            else:
                response = self.session.get(task.url)
        elif task.method == 'POST':
            response = self.session.post(task.url, json=task.body)
        else:
            raise Exception(f'unsupported method {task.method}')

        if response.status_code != 200:
            raise Exception(f'The status code for url {task.url} was {response.status_code}')

        self.session.cookies = response.cookies
        logger.info(f'Succeed download the url {task.url}')
        return response.text
