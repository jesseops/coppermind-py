import os
import uuid
from bson import Binary
from ..models import Ebook
from pymongo import MongoClient
from datetime import datetime
from .base import BaseDB, EbookNotFound


class Mongo(BaseDB):
    def __init__(self):
        self._connection = MongoClient().coppermind

    def get_ebook_file(self, book_id):
        return self._connection.data_files.find_one({'uuid': book_id})

    def store_ebook_file(self, **kwargs):
        mongo_uuid = kwargs.get('uuid') or str(uuid.uuid4())
        if 'file' in kwargs:  # Assume file-like object
            pass
        elif 'path' in kwargs:  # Assume path to ebook on disk
            if os.path.exists(kwargs['path']):
                with open(kwargs['path'], 'rb') as data_file:
                    if kwargs['fmt'].lower() == 'epub':
                        ebook_bin = Binary(data_file.read())
                    else:
                        raise NotImplementedError('Only epub supported for now')
                    self._connection.data_files.insert({'uuid': mongo_uuid,
                                                        'file': ebook_bin,
                                                        'timestamp': datetime.utcnow()})
        return mongo_uuid

    def save_ebook_metadata(self, ebook):
        if not ebook.get('uuid'):
            mongo_uuid = str(uuid.uuid4())
            ebook['identifiers'].append({'identifier': 'coppermind_id', 'value': mongo_uuid})
            ebook['uuid'] = mongo_uuid
        self._connection.metadata.update({'uuid': mongo_uuid}, {'$set': ebook}, upsert=True)
        return mongo_uuid

    def get_ebook(self, identifier):
        data = self._connection.metadata.find_one({'identifiers.value': identifier}, {'_id': 0})
        if data:
            return Ebook.from_dict(data)
        raise EbookNotFound('Unable to locate an ebook for identifier {}'.format(identifier))

    def search_ebooks(self, **query):
        raise NotImplementedError

