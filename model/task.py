import json


class Task:

    @classmethod
    def from_string(cls, content: str) -> 'Task':
        data = json.loads(content)
        return Task(data.get('url', ''), data.get('type', ''), data.get('reference', ''),
                    data.get('method', 'GET'), data.get('params', {}), data.get('body', {}), data.get('metadata', {}))

    def __init__(self, url: str, type_: str, reference: str, method: str = 'GET', params: dict = None,
                 body: dict = None, metadata: dict = None):
        self.method = method.upper()
        self.url = url
        self.type_ = type_
        self.reference = reference
        self.params = params if params else {}
        self.body = body if body else {}
        self.metadata = metadata if metadata else {}

    def __str__(self):
        data = {
            'method': self.method,
            'url': self.url,
            'type': self.type_,
            'reference': self.reference,
            'params': self.params,
            'body': self.body,
            'metadata': self.metadata,
        }
        return json.dumps(data, ensure_ascii=False, sort_keys=True)
