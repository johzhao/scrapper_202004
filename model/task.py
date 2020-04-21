import json


class Task:

    @classmethod
    def from_string(cls, content: str) -> 'Task':
        data = json.loads(content)
        return Task(data.get('url'), data.get('type'), data.get('reference'))

    def __init__(self, url: str, type_: str, reference: str, metadata=None):
        self.url = url
        self.type_ = type_
        self.reference = reference
        self.metadata = metadata if metadata else {}

    def __str__(self):
        data = {
            'url': self.url,
            'type': self.type_,
            'reference': self.reference,
            'metadata': self.metadata,
        }
        return json.dumps(data, ensure_ascii=False, sort_keys=True)
