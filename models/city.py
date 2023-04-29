#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place",
                              backref="cities",  cascade='delete')
    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """getter attribute returns the list of Place instances"""
            from models.place import Place
            all_places = models.storage.all(Place).values()
            place_list = [place for place in all_places
                          if place.city_id == self.id]
            return place_list
