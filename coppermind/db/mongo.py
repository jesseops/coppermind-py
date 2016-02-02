import os
import uuid
from bson import Binary
from ..models import Ebook
from ..tools.parser import file_hash
from pymongo import MongoClient
from datetime import datetime
from .base import BaseDB, EbookNotFound


class Mongo(BaseDB):
    def __init__(self):
        self._connection = MongoClient().coppermind

    def get_ebook_file(self, book_id):
        return self._connection.data_files.find_one({'sha256': book_id})

    def store_ebook_file(self, **kwargs):
        if 'file' in kwargs:  # Assume file-like object
            raise NotImplementedError('Epub only for now')
        elif 'path' in kwargs:  # Assume path to ebook on disk
            if os.path.exists(kwargs['path']):
                sha256 = kwargs.get('sha256') or file_hash(kwargs['path'])
                with open(kwargs['path'], 'rb') as data_file:
                    if kwargs['fmt'].lower() == 'epub':
                        ebook_bin = Binary(data_file.read())
                    else:
                        raise NotImplementedError('Only epub supported for now')
                    self._connection.data_files.insert({'sha256': sha256,
                                                        'file': ebook_bin,
                                                        'timestamp': datetime.utcnow()})
        return sha256

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

