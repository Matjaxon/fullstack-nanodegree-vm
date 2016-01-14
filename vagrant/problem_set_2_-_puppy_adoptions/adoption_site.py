from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Shelter, Puppy, PuppyProfile, Adopter
from adoptions import Adoption, AddPuppy, UpdateCapacities
from sqlalchemy.ext.declarative import declarative_base #used in configuration and class code

app = Flask(__name__)


# Set up ability to query puppyshelter database via Python code.
Base = declarative_base()
engine = create_engine('postgresql:///puppyshelter')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# Show all participating shelters.
@app.route('/shelters/')
def sheltersPage():
	shelters = session.query(Shelter).all()
	return render_template('shelters.html', shelters = shelters)

# Show all available puppies.
@app.route('/puppies/avail')
def availPuppies():
	availPuppies = session.query(Puppy).filter(Puppy.adopter_id == None).order_by(Puppy.name).all()
	return render_template('availpuppies.html', availPuppies = availPuppies)	

@app.route('/puppies/<int:puppy_id>/edit')
def editPuppy(puppy_id):
	editPuppy = session.query(Puppy).filter_by(id = puppy_id).one()
	return "Edit page for " + editPuppy.name


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)