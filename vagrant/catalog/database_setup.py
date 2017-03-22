"""Database setup for the Favorite Sports Venue Application

This script will setup the initialize the schema of the database
"""
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
    """
    Create the table for registered users
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

# class Sports(Base):
#     """
#     Table for type of sports and venues
#     """
#     __tablename__ = 'sports'
#
#     id = Column(Integer, primary_key = True)
#     name = Column(String(200), nullable = False)
#     venues = relationship('Arenas', cascade="save-update, merge, delete")
#
#     @property
#     def serialize(self):
#         """
#         Returns sports venue database information in a serialize format
#         """
#         return {
#             'id': self.id,
#             'name': self.name,
#             'venues': [i.serialize for i in self.venues]
#         }

class Arenas(Base):
    """
    Defines the sports arenas table
    """
    __tablename__ = 'arenas'
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
    description = Column(String)
    image = Column(String(250))
    url = Column(String(250))

    # sports_id = Column(Integer, ForeignKey('sports.id'))
    # sport = relationship('Sports')

    users_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')


    @property
    def serialize(self):
        """
        Returns Arenas database
        """
        return {
            'id': self.id,
            'name': self.name,
            'sports_id': self.sports_id,
            'description': self.description
        }

#Creates Database

engine = create_engine('postgresql://sports:sports@localhost/sportsvenue')

Base.metadata.create_all(engine)
