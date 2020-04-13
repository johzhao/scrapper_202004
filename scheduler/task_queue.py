from typing import Optional

import redis

from model.task import Task


class TaskQueue:

    def __init__(self, redis_url: str, db: int):
        self.redis = redis.Redis.from_url(redis_url, db=db)
        self._task_types = ['']

    def push_task(self, task: Task):
        key = self._get_task_key(task.type_)
        self.redis.rpush(key, str(task))

    def get_top_task(self) -> Optional[Task]:
        for task_type in self._task_types:
            key = self._get_task_key(task_type)
            count = self.redis.llen(key)
            if count == 0:
                continue

            data = self.redis.lindex(key, 0)
            return Task.from_string(data)
        return None

    def drop_top_task(self, type_: str):
        self.redis.lpop(self._get_task_key(type_))

    @staticmethod
    def _get_task_key(type_: str) -> str:
        return f'{type_}_tasks'
