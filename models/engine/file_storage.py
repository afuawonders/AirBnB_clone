#!/usr/bin/python3

"""
This file defines the storage system for
the project.
It will use JSON format to either serialize and deserialize objects
"""

import json
from json.decoder import JSONDecodeError
from .errors import *
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class FileStorage:
    """
   serializes instances to a JSON file and deserializes JSON file to instances:
    """

    """class private varaibles"""
    """dictionary - empty but will store all objects by """
    __objects: dict = {}

    """string - path to the JSON file"""
    __file_path: str = 'file.json'
    models = ("BaseModel", "User", "City", "State", "Place",
              "Amenity", "Review")

    def __init__(self):
        """constructor"""
        pass

    def all(self):
        """ returns the dictionary """
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        serialized = {
            key: val.to_dict()
            for key, val in self.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(serialized))

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists"""
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                key:
                    eval(obj["__class__"])(**obj)
                    for key, obj in deserialized.items()}
        except FileNotFoundError:
            # Handle the FileNotFoundError here if needed
            pass
        except json.JSONDecodeError:
            # Handle the JSONDecodeError here if needed
            pass

    def get_instance_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in FileStorage.models:
            raise ModelNotFoundError(model)
        key = f"{model}.{obj_id}"
        obj = FileStorage.__objects.get(key)
        if obj is None:
            raise InstanceNotFoundError(obj_id, model)
        return obj

    def remove_instance_by_id(self, model, obj_id):
        """Delete an element of model by its id"""
        if model not in FileStorage.models:
            raise ModelNotFoundError(model)
        key = f"{model}.{obj_id}"

        if key not in FileStorage.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del FileStorage.__objects[key]
        self.save()

    def get_all_instances(self, model=""):
        """Find all instances or instances of model"""
        if model and model not in FileStorage.models:
            raise ModelNotFoundError(model)
        results = [str(val) for key, val in FileStorage.__objects.items()
                   if key.startswith(model)]
        return results

    def modify_instance(self, model, iid, field, value):
        """Updates an instance"""
        if model not in FileStorage.models:
            raise ModelNotFoundError(model)

        key = f"{model}.{iid}"
        obj = FileStorage.__objects.get(key)
        if obj is None:
            raise InstanceNotFoundError(iid, model)

        if field in ("id", "updated_at", "created_at"):
            # Not allowed to be updated
            return

        setattr(obj, field, type(getattr(obj, field, value))(value))
        obj.updated_at = datetime.utcnow()
        self.save()
