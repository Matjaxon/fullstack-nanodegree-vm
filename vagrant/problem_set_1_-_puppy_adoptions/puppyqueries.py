from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
import datetime


engine = create_engine('postgresql:///puppyshelter')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Query 1. Query all of the puppies and return the results in ascending
# alphabetical order
allPuppies = session.query(Puppy).order_by(Puppy.name).all()
for puppy in allPuppies:
    print puppy.name

# Query 2.  Query all of the puppies that are less than 6 months old
# organized by the youngest first.
today = datetime.date.today()
sixMosBefore = today - datetime.timedelta(days = 180)
newPuppies = session.query(Puppy).filter(Puppy.dateOfBirth >= sixMosBefore)\
.order_by(desc(Puppy.dateOfBirth)).all()
for puppy in newPuppies:
    print (puppy.name + ' | ' + str(puppy.dateOfBirth))
#need to figure out the time fucntionality for subtracting 6 months

# Query 3.  Query all puppies by ascending weight
allPuppies = session.query(Puppy).order_by(Puppy.weight).all()
for puppy in allPuppies:
    print (puppy.name + ' | ' + str(puppy.weight))

# Query 4.  Query all puppies grouped by the shelter in which they are staying
allPuppies = session.query(Puppy, Shelter).filter(Shelter.id==Puppy.shelter_id)\
.order_by('Shelter.name', 'Puppy.name').all()
for puppy, shelter in allPuppies:
    print(puppy.name + ' | ' + shelter.name + ' | ' + str(shelter.id))
