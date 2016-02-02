import unittest
from coppermind.db.mongo import Mongo
from . import test_models_ebook

class test_DB_Mongo(test_models_ebook.testEbook):

    db = Mongo

    def test_ebook(self):
        pass


if __name__ == "__main__":
    unittest.main()
