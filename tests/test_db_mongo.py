import unittest
import hashlib
from . import test_models_ebook
from coppermind.common.db.mongo import Mongo


# class test_DB_Mongo(test_models_ebook.testEbook):

#     db = Mongo()

#     def setUp(self):
#         self.db._connection.metadata.create_index('uuid', unique=True)
#         self.db._connection.data_files.create_index('sha256', unique=True)

#     def tearDown(self):
#         """
#         Cleanup db after unittests
#         """
#         self.db._connection.metadata.drop()
#         self.db._connection.data_files.drop()


if __name__ == "__main__":
    # unittest.main()
    pass
