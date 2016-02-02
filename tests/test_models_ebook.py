import logging
import unittest
from coppermind.models import Ebook


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
        ebook = Ebook.from_file('./sample_ebooks/peter_pan.epub')
        self.assertIsInstance(ebook, Ebook)

    def test_db(self):
        if not self.db:
            raise unittest.SkipTest('DB tests will only run if DB is set')
        self.assertIsNotNone(self.db)


if __name__ == "__main__":
    unittest.main()
