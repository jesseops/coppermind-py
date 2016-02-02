import unittest
from coppermind.db.mongo import Mongo
from coppermind.models.ebook import Ebook
from . import test_models_ebook

class test_DB_Mongo(test_models_ebook.testEbook):

    db = Mongo()

    def test_ebook(self):
        ebook = Ebook.from_file(self.sample_ebook)
        ebook_id = self.db.save_ebook(ebook, path=self.sample_ebook)

        new_ebook = self.db.get_ebook(ebook_id)
        self.assertEqual(new_ebook.author, ebook.author)
        self.assertIsNotNone(self.db.get_ebook_file(new_ebook.storage['mongo']))


if __name__ == "__main__":
    unittest.main()
