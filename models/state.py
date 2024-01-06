#!/usr/bin/python3
""" State Module for HBNB project """
import models
import os
import sqlalchemy
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="states",
                              cascade="all, delete")
    else:
        name = ""

    def _init_(self, *args, **kwargs):
        """initializing state class"""
        super()._init_(*args, **kwargs)

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """getter method to retrieve city instance"""
            city_values = models.storage.all("City").values()
            city_list = []
            for c in city_values:
                if c.state_id == self.id:
                    city_list.append(c)
            return city_list
