import os

import sys #provides a number of functions and variables that can be used to manipulate different parts
#  of the python runtime environment.

from sqlalchemy import Column, ForeignKey, Integer, String #imports classes from SQL Alchemy.
##Used for mapper code.

from sqlalchemy.ext.declarative import declarative_base #used in configuration and class code

from sqlalchemy.orm import relationship #used in mapper

from sqlalchemy import create_engine

Base = declarative_base()  #let sql alchemy know that our clsses are specialy sql alchemy classes
#  that correspond to tables in db

class Restaurant(Base):  #setting up sql tables via python class
	__tablename__ = 'restaurant'
	name = Column(
		String(80), nullable = False)

	id = Column(
		Integer, primary_key = True)

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name' : self.name,
		}


class MenuItem(Base):  #setting up sql tables via python class
	__tablename__ = 'menu_item'
	name = Column(
		String(80), nullable = False)
	id = Column(
		Integer, primary_key = True)
	course = Column(
		String(250))
	description = Column(String(250))
	price = Column(
		String(8))
	restaurant_id = Column(
		Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		# Returns object data in easily searialeable format
		return {
			'name' : self.name,
			'description' : self.description,
			'id' : self.id,
			'price' : self.price,
			'course' : self.course,
		}



##### instert at end of file ######

engine = create_engine('postgresql:///restaurantmenu') #using sqlite 3

Base.metadata.create_all(engine)  #goes into db and addes new tables.
