import uuid
import logging
from ..tools import ebook_parser
from ..tools import SVCObj
from ..db.base import EbookNotFound


class Ebook:
    """
    Should contain all knowledge about a given ebook and
    operations available for ebooks

    Actual ebook file should be stored in DB with a UUID which allows returning
    the file when required. It isn't necessary to keep the ebook in memory
    """

    def __init__(self, **ebook_data):
        self._metadata = ebook_data

    def save(self, db):
        if not self._metadata.get('uuid'):
            try:
                book_id = db.get_ebook(self._metadata['sha256sum'])
            except EbookNotFound:
                self._metadata['uuid'] = str(uuid.uuid4())
        db.save_ebook(self, **self.serialize())

    @classmethod
    def from_dict(self, ebook_data):
        """
        Instantiate an ebook instance from provided dict
        """
        return Ebook(**ebook_data)

    @classmethod
    def from_file(self, ebook_file):
        """
        Instantiate an ebook object from an actual ebook file (epub, mobi, etc)
        Metadata should be parsed and everything passed back into the object appropriately
        """
        metadata = ebook_parser(ebook_file)
        return Ebook(**metadata)

    def serialize(self):
        """
        Return an easily storable representation of an `Ebook` object
        Should be able to rehydrate from serialized data
        """
        return self._metadata

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._metadata['format']}::{self._metadata['sha256sum']})>"

    def __getattr__(self, attr):
        try:
            return self._metadata[attr]
        except KeyError as e:
            raise AttributeError("{} has no attribute {}".format(self, e))
