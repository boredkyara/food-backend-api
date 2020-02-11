import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    type = Column(String(250))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
        }


class Meal(Base):
    __tablename__ = 'meal'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    image_link = Column(String(250), nullable=True)
    price = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'image_link': self.image_link,
            'price': self.price,
            'name': self.name,
            'description': self.description
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///restaurant-collection.db')
Base.metadata.create_all(engine)

