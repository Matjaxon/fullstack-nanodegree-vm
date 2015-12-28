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

class Employee(Base):
	__tablename__ = 'employee'
	name = Column(
		String(250), nullable = False)
	id = Column(
		Integer, primary_key = True)

class Address(Base):
	__tablename__ = 'adress'
	street = Column(
		String(80), nullable = False)
		zip = Column(
			String(5), nullable = False)
		id = Column(Integer, primary_key = True)
		employee_id = Column(
			Integer, ForeignKey('employee.id'))
		employee = relationship(Employee)



##### instert at end of file ######

engine = create_engine('sqlite:///restaurantmenu.db') #using sqlite 3

Base.metadata.create_all(engine)  #goes into db and addes new tables.