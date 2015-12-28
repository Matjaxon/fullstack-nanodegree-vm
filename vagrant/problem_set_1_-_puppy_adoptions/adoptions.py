from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy, Adopter
# from puppypopulator import CreateRandomAge, CreateRandomWeight
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('postgresql:///puppyshelter')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# create an adoption by updating the puppy adopter_id and adding adoption date.
def Adoption(puppy_id, adopter_id, adoption_date = ''):
    adopted_puppy = session.query(Puppy).filter(Puppy.id == puppy_id).one()
    print (str(adopted_puppy.id)+ ' | ' + adopted_puppy.name)
    if adoption_date == '':
        adoption_date = datetime.date.today()
    adopted_puppy.adopter_id = adopter_id
    adopted_puppy.adoption_date = adoption_date
    session.add(adopted_puppy)
    session.commit()
    UpdateCapacities()

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

def UpdateCapacities():

    '''Refreshes the remaining capacities of all shelters. '''

    #prints out shelter_id, shelter_name, count of puppies at each shelter
    puppy_count = session.query(Puppy.shelter_id, Shelter.name,\
     func.count(Puppy.shelter_id), Shelter.capacity, Shelter.remaining_capacity)\
     .filter(Puppy.shelter_id == Shelter.id, Puppy.adopter_id == None).\
     group_by(Puppy.shelter_id, Shelter.name, Shelter.capacity, Shelter.remaining_capacity)\
     .order_by(Puppy.shelter_id).all()
    for shelter in puppy_count:

        # determine the shelter for which the capacity will be updated.
        updating_shelter = session.query(Shelter).filter(Shelter.id == shelter[0])\
        .one()

        # determine the remaining capacity of the shelter.
        remaining_capacity = shelter.capacity - shelter[2]
        updating_shelter.remaining_capacity = remaining_capacity
        session.add(updating_shelter)
        session.commit()
        print shelter
    print "All shelter capacities refreshed."

# # add 5 random adoptions for available puppies
def FiveAdoptions():
    for i in range(5):
        adopters = session.query(Adopter).all()
        adopter = randint(1, len(adopters))
        available_puppies = session.query(Puppy).filter(Puppy.adopter_id == None).all()
        adopted_puppy = randint(1, len(available_puppies))
        Adoption(adopted_puppy, adopter)

def AddPuppy(puppy_name, puppy_gender, new_puppy_shelter = '', puppy_picture = ''):
    if new_puppy_shelter == '':
        most_open_shelter = session.query(Puppy.shelter_id, Shelter.name,\
         func.count(Puppy.shelter_id), Shelter.capacity, Shelter.remaining_capacity)\
         .filter(Puppy.shelter_id == Shelter.id, Puppy.adopter_id == None).\
         group_by(Puppy.shelter_id, Shelter.name, Shelter.capacity, Shelter.remaining_capacity)\
         .order_by(desc(Shelter.remaining_capacity)).first()

        new_puppy_shelter = most_open_shelter.shelter_id

    new_puppy = Puppy(name = puppy_name, gender = puppy_gender, dateOfBirth = CreateRandomAge(),picture = puppy_picture ,shelter_id= new_puppy_shelter, weight= CreateRandomWeight())
    session.add(new_puppy)
    session.commit()
    print puppy_name + ' added to ' + most_open_shelter.name
    UpdateCapacities()

FiveAdoptions()
# AddPuppy('Grace', 'female')
# AddPuppy('Jax', 'male')
# AddPuppy('Earl', 'male')
# AddPuppy('Phoebe', 'female')
# AddPuppy('Miller', 'male')
# AddPuppy('Joe', 'male')
# AddPuppy('Alfy', 'male')
# AddPuppy('Lexi', 'female')
# AddPuppy('Phillip', 'male')
# AddPuppy('Kane', 'male')
# UpdateCapacities()
