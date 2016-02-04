import os
import logging
import unittest
from coppermind.models import Ebook
from coppermind.tools.parser import file_hash, _mobi_parser, InvalidEbookFile


fake_ebook = {"title": 'FooBar',
              "author": 'Baz, Foo',
              "year_published": 2016,
              "publisher": '',
              "genre": 'Testcase'}


class testEbook(unittest.TestCase):
    """
    Test the ebook class
    Should perform any action the user is able to perform
    on the ebook and validate action succeeds
    """
    db = None  # For DB testing
    sample_ebook = os.path.join(os.path.dirname(__file__), 'sample_ebooks/peter_pan.epub')

    def test_from_dict(self):
        ebook = Ebook.from_dict(fake_ebook)
        self.assertIsInstance(ebook, Ebook)

    def test_author(self):
        ebook = Ebook.from_dict(fake_ebook)
        self.assertEqual(ebook.author, 'Baz, Foo')

    def test_serialize(self):
        ebook = Ebook.from_dict(fake_ebook)
        serialized = ebook.serialize()
        self.assertIsInstance(serialized, dict)
        self.assertEqual(serialized, fake_ebook)

    def test_from_file(self):
        ebook = Ebook.from_file(self.sample_ebook)
        self.assertIsInstance(ebook, Ebook)

    def test_save_ebook(self):
        if not self.db:
            raise unittest.SkipTest('DB tests will only run if DB is set')
        ebook = Ebook.from_file(self.sample_ebook)
        ebook_id = self.db.save_ebook(ebook, path=self.sample_ebook)

        new_ebook = self.db.get_ebook(ebook_id)
        self.assertEqual(new_ebook.author, ebook.author)
        self.assertIsNotNone(self.db.get_ebook_file(new_ebook.storage['mongo']))

    def test_get_ebook(self):
        if not self.db:
            raise unittest.SkipTest('DB tests will only run if DB is set')
        sha256 = file_hash(self.sample_ebook)
        ebook = Ebook.from_file(self.sample_ebook)
        ebook_id = self.db.save_ebook(ebook, path=self.sample_ebook)
        self.assertIsNotNone(self.db.get_ebook_file(sha256))

    def test_duplicate(self):
        if not self.db:
            raise unittest.SkipTest('DB tests will only run if DB is set')
        ebook = Ebook.from_file(self.sample_ebook)
        self.db.save_ebook(ebook, path=self.sample_ebook)
        with self.assertRaises(Exception):
            ebook2 = Ebook.from_file(self.sample_ebook)
            self.db.save_ebook(ebook2, path=self.sample_ebook)

    def test_mobi(self):
        with self.assertRaises(InvalidEbookFile):
            _mobi_parser(self.sample_ebook)
        _mobi_parser(self.sample_ebook.replace('epub', 'mobi'))

if __name__ == "__main__":
    unittest.main()
