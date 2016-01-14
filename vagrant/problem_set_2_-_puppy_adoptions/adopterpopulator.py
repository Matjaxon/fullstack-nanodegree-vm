from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy, Adopter
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('postgresql:///puppyshelter')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

male_firstname = ['John', 'Mike', 'Matt', 'Kyle', 'Stephen', 'Alex']
male_lastname = ['Johnson', 'Smith', 'Morris', 'Jackson', 'Peterson']

female_firstname = ['Samantha', 'Melissa', 'Michelle', 'Stephanie', 'Amy']
female_lastname = ['Lawerence', 'Downy', 'Williamson', 'Smith']

def CreateDOB():
    year = randint(1970,1998)
    month = randint(1,12)
    if month == 2:
        day = randint(1,28)
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        day = randint(1, 31)
    else:
        day = randint(1, 30)
    dob = datetime.date(year, month, day)
    return dob

def CreateAdopter():
    if randint(0,1) == 0:
        gender = 'male'
    else:
        gender = 'female'
    if gender == 'male':
        first = male_firstname[randint(0, len(male_firstname)-1)]
        last = male_lastname[randint(0, len(male_lastname)-1)]
    else:
        first = female_firstname[randint(0, len(female_firstname)-1)]
        last = female_lastname[randint(0, len(female_lastname)-1)]
    dob = CreateDOB()
    return first, last, dob

for i in range(10):
    first, last, dob = CreateAdopter()
    new_adopter = Adopter(firstname = first, lastname = last, dateOfBirth = dob)
    session.add(new_adopter)
    session.commit()
