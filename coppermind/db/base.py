import uuid
import logging
from abc import ABCMeta, abstractmethod


class BaseDB(metaclass=ABCMeta):
    """
    Base for all DB classes. Defines a standard interface
    allowing multiple DB implementations without requiring
    any additional code changes.

    Unittests for any DB implementation should simply be
    running the ebook unittest against that implementation
    """

    @abstractmethod
    def get_ebook_file(self, uuid):
        """
        Return actual ebook file by UUID
        """

    @abstractmethod
    def store_ebook_file(self, ebook_file):
        """
        Store ebook file, return UUID for later lookup
        """

    @abstractmethod
    def save_ebook(self, ebook):
        """
        Store ebook object
        """

    @abstractmethod
    def get_ebook(self, identifier):
        """
        Return a single ebook by any identifier
        ISBN, Coppermind UUID, etc are all valid

        Unittests should search for all supported identifiers
        """

    @abstractmethod
    def search_ebooks(self, **query):
        """
        Locate ebooks matching query
        """
