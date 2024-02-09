#!/usr/bin/python3
"""Unittest module for the Amenity Class."""

import unittest
from datetime import datetime
import time
from models.amenity import Amenity
import re
import json
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):

    """Test Cases for the Amenity class."""

    def setUp(self):
        """Test methods set up."""
        pass

    def tearDown(self):
        """Test methods tear down."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """FileStorage data resets."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_8_instantiation(self):
        """Amenity class instantiation tests."""

        bns = Amenity()
        self.assertEqual(str(type(bns)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(bns, Amenity)
        self.assertTrue(issubclass(type(bns), BaseModel))


if __name__ == "__main__":
    unittest.main()
