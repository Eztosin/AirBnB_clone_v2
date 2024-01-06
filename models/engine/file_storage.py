#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        json_obj = {}
        for key in self.__objects:
            json_obj[key] = self.__objects[key].to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(json_obj, file)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {'BaseModel': BaseModel, 'User': User,
                   'Place': Place,'State': State, 'City': City,
                   'Amenity': Amenity, 'Review': Review}
        try:
            with open(self.__file_path, "r") as file:
                temp = json.load(file)
            for key in temp:
                self.__objects[key] = classes[temp[key]["__class__"]](**temp[key])
        except:
            pass

    def delete(self, obj=None):
        """deletes objects if exists"""
        if obj is not None:
            del self.__objects["{}.{}".format(obj.__class__.__name__,
                                              obj.id)]
            self.save()

    def close(self):
        """calls reload method"""
        self.reload()
