#!/usr/bin/python3
""" City Module for HBNB project """
import models
from models.base_model import BaseModel
from models.base_model import Base
import sqlalchemy
from sqlalchemy import Column, String
import os
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        state_id = Column(String(128), nullable=False)
        name = Column(String(60), ForeignKey("states.id"),
                      nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
    else:
        name = ""
        state_id = ""

    def _init_(self, *args, **kwargs):
        "initializing city class"
        super()._init_(*args, **kwargs)
