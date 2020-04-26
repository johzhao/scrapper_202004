import logging

from mongoengine import Document
from mongoengine import connect


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# Remove this class
class Storage:

    def __init__(self, database: str, host: str, port: int):
        connect(database, host=host, port=port)

    def save_content(self, content: Document, type_: str):
        logger.info(f'Save type {type_}, content {content}')
        content.save()
