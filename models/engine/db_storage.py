#!/usr/bin/python3
"""DBStorage - States and Cities"""

from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

class_name = { "Amenity": Amenity,
               "City": City,
               "Place": Place,
               "State": State,
               "Review": Review,
               "User": User
}


class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initializing the object"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, passwd, host,
                                              database))
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns dictionary of objects"""
        if not self.__session:
            self.reload()
        objs = {}
        if type(cls) == str:
            cls = class_name.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objs[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for cls in class_name.values():
                for obj in self.__session.query(cls):
                    objs[obj.__class__.__name__ + "." + obj.id] = obj
        return objs

    def reload(self):
        """reloads objects"""
        new_session = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(new_session)

    def new(self, obj):
        """creates an object"""
        self.__session.add(obj)

    def save(self):
        """saves an ongoing session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """closes ongoing session"""
        self.__session.remove()

    def get(self, cls, id):
        """retrieves object"""
        if cls is not None and type(cls) is str and id is not None and type(id) is str and cls in class_name:
            cls = class_name[cls]
            objs = self.__session.query(cls).filter(cls.id
                                                    == id).first()
            return objs
        else:
            return None

    def count(self, cls=None):
        """counts objects in storage"""
        total_objs = 0
        if type(cls) == str and cls in class_name:
            cls = class_name[cls]
            total_objs = self.__session.query(cls).count()
        elif cls is None:
            for cls in class_name.values():
                total_objs += self.__session.query(cls).count()
        return total_objs
