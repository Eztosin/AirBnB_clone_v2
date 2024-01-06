#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from models.review import Review
import os
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(1024), nullable=False)
        description = Column(String(1024), nullable=False)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        place_amenity = Table("place_amenity", Base.metadata,
                              Column("place_id", String(60),
                                     ForeignKey("place.id"),
                                     primary_key=True,
                                     nullable=False),
                              Column("amenity_id", String(60),
                                     ForeignKey("amenities.id"),
                                     primary_key=True, nullable=False))
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, backref="places")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """getter method for reviews"""
            from models import storage
            rev_list = []
            all_reviews = storage.all(Review)
            for value in all_reviews.values():
                if value.place_id == self.id:
                    rev_list.append(value)
            return rev_list

        @property
        def amenities(self):
            """getter method for amenities"""
            from models import storage
            from models.amenity import Amenity
            amnty_list = []
            all_amenities = storage.all(Amenity)
            for value in all_amenities.values():
                if value.id == self.amenity_ids:
                    amnty_list.append(value)
            return amnty_list

        @amenities.setter
        def amenities(self, value):
            """setter method for amenities"""
            from models import storage
            from models.amenity import Amenity
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
        
