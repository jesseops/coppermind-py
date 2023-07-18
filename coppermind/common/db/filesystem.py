import os
import uuid
import sqlite3
import yact
from shutil import copy2
from ..models import Ebook
from ..tools.parser import file_hash
from datetime import datetime
from .base import BaseDB, EbookNotFound


class FileSystem(BaseDB):

    def __init__(self):
        self._storage_directory = os.path.join(os.path.pardir, 'coppermind-storage')
        if not os.path.exists(self._storage_directory):
            os.makedirs(self._storage_directory)
        self._connection = sqlite3.connect(os.path.join(self._storage_directory, self.config.get('filename', 'coppermind.db')), check_same_thread=False)
        with self._connection:
            self._connection.execute(""" CREATE TABLE IF NOT EXISTS books (
                                        id text PRIMARY KEY,
                                        author text NOT NULL,
                                        title text NOT NULL,
                                        format text NOT NULL
                                         ); """)
            self._connection.execute(""" CREATE TABLE IF NOT EXISTS storage (
                                        id text PRIMARY KEY,
                                        sha256sum text NOT NULL,
                                        uri text NOT NULL
                                         ); """)

    def get_ebook_file(self, book_id):
        with self._connection:
            path = self._connection.execute("SELECT uri FROM storage where id = ?", (book_id,))
        with open(path) as book:
            return book.read()

    def store_ebook_file(self, **kwargs):
        if 'file' in kwargs:  # Assume file-like object
            raise NotImplementedError('Epub only for now')
        elif 'path' in kwargs:  # Assume path to ebook on disk
            if os.path.exists(kwargs['path']):
                sha256 = kwargs.get('sha256') or file_hash(kwargs['path'])
                dest_path = os.path.join(self._storage_directory, sha256)
                copy2(kwargs['path'], dest_path)
        with self._connection:
            self._connection.execute("INSERT INTO storage VALUES(?, ?, ?);", (kwargs['uuid'], sha256, f"file://{dest_path}"))
        return f"file://{dest_path}"

    def save_ebook_metadata(self, ebook):
        try:
            book_id = ebook.uuid
        except KeyError:
            book_id = str(uuid.uuid4())
            ebook._metadata['uuid'] = book_id
        with self._connection:
            self._connection.execute("INSERT INTO books VALUES(?, ?, ?, ?) on conflict(id) do nothing;", (book_id, ebook.author, ebook.title, ebook.format))
        return book_id

    def get_ebook(self, identifier):
        cursor = self._connection.execute("SELECT books.id, author, title, uri, sha256sum FROM storage JOIN books on books.id = storage.id WHERE sha256sum = ?;", (identifier,))
        results = cursor.fetchone()
        if results:
            return Ebook.from_dict(dict(zip(('uuid', 'author', 'title', 'path'), results)))
        raise EbookNotFound('Unable to locate an ebook for identifier {}'.format(identifier))

    def search_ebooks(self, **query):
        raise NotImplementedError
