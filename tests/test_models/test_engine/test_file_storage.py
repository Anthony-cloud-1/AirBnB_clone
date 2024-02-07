#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bamo = BaseModel()
        user = User()
        state = State()
        pla = Place()
        city = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(bamo)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(pla)
        models.storage.new(city)
        models.storage.new(amen)
        models.storage.new(rev)
        self.assertIn("BaseModel." + bamo.id, models.storage.all().keys())
        self.assertIn(bamo, models.storage.all().values())
        self.assertIn("User." + user.id, models.storage.all().keys())
        self.assertIn(user, models.storage.all().values())
        self.assertIn("State." + state.id, models.storage.all().keys())
        self.assertIn(state, models.storage.all().values())
        self.assertIn("Place." + pla.id, models.storage.all().keys())
        self.assertIn(pla, models.storage.all().values())
        self.assertIn("City." + city.id, models.storage.all().keys())
        self.assertIn(city, models.storage.all().values())
        self.assertIn("Amenity." + amen.id, models.storage.all().keys())
        self.assertIn(amen, models.storage.all().values())
        self.assertIn("Review." + rev.id, models.storage.all().keys())
        self.assertIn(rev, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bamo = BaseModel()
        user = User()
        state = State()
        pla = Place()
        city = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(bamo)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(pla)
        models.storage.new(city)
        models.storage.new(amen)
        models.storage.new(rev)
        models.storage.save()
        r_text = ""
        with open("file.json", "r") as f:
            r_text = f.read()
            self.assertIn("BaseModel." + bamo.id, r_text)
            self.assertIn("User." + user.id, r_text)
            self.assertIn("State." + state.id, r_text)
            self.assertIn("Place." + pla.id, r_text)
            self.assertIn("City." + city.id, r_text)
            self.assertIn("Amenity." + amen.id, r_text)
            self.assertIn("Review." + rev.id, r_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bamo = BaseModel()
        user = User()
        state = State()
        pla = Place()
        city = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(bamo)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(pla)
        models.storage.new(city)
        models.storage.new(amen)
        models.storage.new(rev)
        models.storage.save()
        models.storage.reload()
        objct = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bamo.id, objct)
        self.assertIn("User." + user.id, objct)
        self.assertIn("State." + state.id, objct)
        self.assertIn("Place." + pla.id, objct)
        self.assertIn("City." + city.id, objct)
        self.assertIn("Amenity." + amen.id, objct)
        self.assertIn("Review." + rev.id, objct)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
