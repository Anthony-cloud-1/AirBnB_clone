#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bamo1 = BaseModel()
        bamo2 = BaseModel()
        self.assertNotEqual(bamo1.id, bamo2.id)

    def test_two_models_different_created_at(self):
        bamo1 = BaseModel()
        sleep(0.05)
        bamo2 = BaseModel()
        self.assertLess(bamo1.created_at, bamo2.created_at)

    def test_two_models_different_updated_at(self):
        bamo1 = BaseModel()
        sleep(0.05)
        bamo2 = BaseModel()
        self.assertLess(bamo1.updated_at, bamo2.updated_at)

    def test_str_representation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        bamo = BaseModel()
        bamo.id = "123456"
        bamo.created_at = bamo.updated_at = dtime
        bamostr = bamo.__str__()
        self.assertIn("[BaseModel] (123456)", bamostr)
        self.assertIn("'id': '123456'", bamostr)
        self.assertIn("'created_at': " + dtime_repr, bamostr)
        self.assertIn("'updated_at': " + dtime_repr, bamostr)

    def test_args_unused(self):
        bamo = BaseModel(None)
        self.assertNotIn(None, bamo.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dt.isoformat()
        bamo = BaseModel(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(bamo.id, "345")
        self.assertEqual(bamo.created_at, dtime)
        self.assertEqual(bamo.updated_at, dtime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dt.isoformat()
        bamo = BaseModel("12", id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(bamo.id, "345")
        self.assertEqual(bamo.created_at, dtime)
        self.assertEqual(bamo.updated_at, dtime)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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

    def test_one_save(self):
        bamo = BaseModel()
        sleep(0.05)
        first_updated_at = bamo.updated_at
        bamo.save()
        self.assertLess(first_updated_at, bamo.updated_at)

    def test_two_saves(self):
        bamo = BaseModel()
        sleep(0.05)
        first_updated_at = bamo.updated_at
        bamo.save()
        second_updated_at = bamo.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bamo.save()
        self.assertLess(second_updated_at, bamo.updated_at)

    def test_save_with_arg(self):
        bamo = BaseModel()
        with self.assertRaises(TypeError):
            bamo.save(None)

    def test_save_updates_file(self):
        bamo = BaseModel()
        bamo.save()
        bamoid = "BaseModel." + bamo.id
        with open("file.json", "r") as f:
            self.assertIn(bamoid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        bamo = BaseModel()
        self.assertTrue(dict, type(bamo.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bamo = BaseModel()
        self.assertIn("id", bamo.to_dict())
        self.assertIn("created_at", bamo.to_dict())
        self.assertIn("updated_at", bamo.to_dict())
        self.assertIn("__class__", bamo.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bamo = BaseModel()
        bamo.name = "Holberton"
        bamo.my_number = 98
        self.assertIn("name", bamo.to_dict())
        self.assertIn("my_number", bamo.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bamo = BaseModel()
        bamo_dict = bamo.to_dict()
        self.assertEqual(str, type(bamo_dict["created_at"]))
        self.assertEqual(str, type(bamo_dict["updated_at"]))

    def test_to_dict_output(self):
        dtime = datetime.today()
        bamo = BaseModel()
        bamo.id = "123456"
        bamo.created_at = bamo.updated_at = dtime
        todict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat()
        }
        self.assertDictEqual(bamo.to_dict(), todict)

    def test_contrast_to_dict_dunder_dict(self):
        bamo = BaseModel()
        self.assertNotEqual(bamo.to_dict(), bamo.__dict__)

    def test_to_dict_with_arg(self):
        bamo = BaseModel()
        with self.assertRaises(TypeError):
            bamo.to_dict(None)


if __name__ == "__main__":
    unittest.main()
