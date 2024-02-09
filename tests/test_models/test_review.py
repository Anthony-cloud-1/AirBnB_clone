#!/usr/bin/python3
"""Unittest module for the Review Class."""

import unittest
from datetime import datetime
import time
from models.review import Review
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    """Test Cases for the Review class."""

    def setUp(self):
        """Test methods set up."""
        pass

    def tearDown(self):
        """Test methods tear down."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """FileStorage data reset."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_8_instantiation(self):
        """Tests instantiation of Review class."""

        bns = Review()
        self.assertEqual(str(type(bns)), "<class 'models.review.Review'>")
        self.assertIsInstance(bns, Review)
        self.assertTrue(issubclass(type(bns), BaseModel))


if __name__ == "__main__":
    unittest.main()
