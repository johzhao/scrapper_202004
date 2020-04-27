import datetime
import json

from model.sina_topic_v2 import WeiboTopicDetailItem
from model.task import Task
from parser.parser import Parser


class TopicDetailParser(Parser):

    def __init__(self):
        super().__init__()

    def parse(self, task: Task, content: str):
        data = json.loads(content)
        data = data['data']
        items = []
        for record in zip(data['read'], data['me'], data['ori']):
            time0 = record[0]['time']
            time1 = record[1]['time']
            time2 = record[2]['time']
            if not (time0 == time1 == time2):
                raise Exception(f'Failed to parse topic data from {record}')
            date = datetime.datetime.strptime(time0, '%m-%d')
            date = datetime.datetime(2020, date.month, date.day)

            read_count = record[0]['value']
            discus_count = int(record[1]['value'])
            create_count = int(record[2]['value'])

            item = WeiboTopicDetailItem()
            item.keyword = task.metadata['keyword']
            item.title = task.metadata['title']
            item.date = date
            item.read_count = read_count
            item.discus_count = discus_count
            item.create_count = create_count
            items.append(item)

        for item in items:
            yield item
