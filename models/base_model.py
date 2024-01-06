#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import os
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

time_frmt = "%Y-%m-%dT%H:%M:%S.%f"

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializing the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == "__class__":
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at,
                                                    time_frmt)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at
                                                    ,time_frmt)

    def __str__(self):
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__,
                                         self.id, self.__dict__)

    def save(self):
        """Updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns dictionary containing all keys/values of instance"""
        new_dict = {}
        new_dict.update(self.__dict__)
        new_dict.update({"__class__": self.__class__.__name__})
        new_dict["created_at"] = new_dict["created_at"].isoformat()
        new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict.pop("_sa_instance_state", None)
        return new_dict

    def delete(self):
        """deletes current instance from storage"""
        models.storage.delete(self)
