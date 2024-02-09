#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects 'obj' with 'key' <obj_class_name>.id"""
        name_ocls = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(name_ocls, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        obdict = FileStorage.__objects
        o_dict = {obj: obdict[obj].to_dict() for obj in obdict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(o_dict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects when it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                o_dict = json.load(f)
                for ob in o_dict.values():
                    name_cls = ob["__class__"]
                    del ob["__class__"]
                    self.new(eval(name_cls)(**ob))
        except FileNotFoundError:
            return
