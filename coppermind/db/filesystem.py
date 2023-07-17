import os
import uuid
import yact
from shutil import copy2
from ..models import Ebook
from ..tools.parser import file_hash
from datetime import datetime
from .base import BaseDB, EbookNotFound


class Filesystem(BaseDB):
    def __init__(self):
        self.filepath = os.path.join(os.path.pardir, 'coppermind-storage')
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        self.mapping = yact.from_file('map.yaml', self.filepath)

    def get_ebook_file(self, book_id):
        path = self.mapping.get(book_id)['filepath']
        with open(os.path.join(self.filepath, path)) as book:
            return book.read()

    def store_ebook_file(self, **kwargs):
        if 'file' in kwargs:  # Assume file-like object
            raise NotImplementedError('Epub only for now')
        elif 'path' in kwargs:  # Assume path to ebook on disk
            if os.path.exists(kwargs['path']):
                sha256 = kwargs.get('sha256') or file_hash(kwargs['path'])
                copy2(kwargs['path'], os.path.join(self.filepath, sha256, os.path.sep))
        return sha256

    def save_ebook_metadata(self, ebook):
        # if not ebook.get('uuid'):
        #     mongo_uuid = str(uuid.uuid4())
        #     ebook['identifiers'].append({'identifier': 'coppermind_id', 'value': mongo_uuid})
        #     ebook['uuid'] = mongo_uuid
        # self._connection.metadata.update_one({'uuid': mongo_uuid}, {'$set': ebook}, upsert=True)
        # return mongo_uuid
        pass

    def get_ebook(self, identifier):
        
        data = self._connection.metadata.find_one({'identifiers.value': identifier}, {'_id': 0})
        if data:
            return Ebook.from_dict(data)
        raise EbookNotFound('Unable to locate an ebook for identifier {}'.format(identifier))

    def search_ebooks(self, **query):
        raise NotImplementedError
