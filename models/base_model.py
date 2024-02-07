#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Represents a BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused args.
            **kwargs (dict): Key/value args.
        """
        
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        dtime = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, dtime)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)

    def save(self):
        """Update 'updated_at' with current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """Return the print/str representation."""
        name_cls = self.__class__.__name__
        return "[{}] ({}) {}".format(name_cls, self.id, self.__dict__)

    def to_dict(self):
        """Return the dictionary.

        Includes key/value pair __class__ representing
        the class name of the object.
        """
        o_dict = self.__dict__.copy()
        o_dict["created_at"] = self.created_at.isoformat()
        o_dict["updated_at"] = self.updated_at.isoformat()
        o_dict["__class__"] = self.__class__.__name__
        return o_dict
