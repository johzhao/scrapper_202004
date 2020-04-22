import abc

from model.task import Task


class Parser(abc.ABC):

    def __init__(self, delegate):
        self.delegate = delegate

    @abc.abstractmethod
    def parse(self, task: Task, content: str):
        return NotImplemented
