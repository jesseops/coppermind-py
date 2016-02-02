import logging
from ..tools import ebook_parser


class Ebook:
    """
    Should contain all knowledge about a given ebook and
    operations available for ebooks

    Actual ebook file should be stored in DB with a UUID which allows returning
    the file when required. It isn't necessary to keep the ebook in memory
    """

    def __init__(self, **ebook_data):
        for k, v in ebook_data.items():
            self.__dict__[k] = v  # quickly set all attrs, rewrite once model stabilizes

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
        return Ebook(**metadata, ebook_file=ebook_file)

    def serialize(self):
        """
        Return an easily storable representation of an `Ebook` object
        Should be able to rehydrate from serialized data
        """
        return self.__dict__
