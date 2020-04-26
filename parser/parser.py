import abc

from model.task import Task


class Parser(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, task: Task, content: str):
        return NotImplemented
