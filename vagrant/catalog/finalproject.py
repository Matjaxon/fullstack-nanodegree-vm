from flask import Flask
from flask import render_template
from flask import url_for
from flask import request  # obtain requests from forms
from flask import redirect  # automatically redirect after after another event.
from flask import flash # allows for flash notifications that will only appear once.
from flask import jsonify # return json for API requests.  Easily configure an API endpoint.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


## Frequently used queries for app. ##
def queryRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
	return restaurant

def queryItem(menu_id):
	item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
	return item

def itemsByCourse(restaurant_id, course):
	items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id,
		MenuItem.course == course).order_by(MenuItem.name).all()
	return items

## End of frequently used queries for app. ##


## Web App Routes. ##

# See all restaurants.
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
	return render_template('restaurants.html', restaurants = restaurants)

# Create a new restaurant.
@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash(newRestaurant.name + " successfully created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')

# Edit an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = queryRestaurant(restaurant_id)
	if request.method == 'POST':
		restaurant.name = request.form['name']
		session.commit()
		flash(restaurant.name + " successfully updated!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant = restaurant)

# Delete an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = queryRestaurant(restaurant_id)
	if request.method == 'POST':
		
		# To delete the restaurant, all foreign keyed menu items must also be deleted.
		itemsToDelete = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
		for item in itemsToDelete:
			session.delete(item)

		session.delete(restaurant)
		session.commit()
		flash(restaurant.name + " successfully deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant = restaurant)

# Show the menu for a given restaurant.
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = queryRestaurant(restaurant_id)
	items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
	appetizers = itemsByCourse(restaurant_id, 'Appetizer')
	entrees = itemsByCourse(restaurant_id, 'Entree')
	desserts = itemsByCourse(restaurant_id, 'Dessert')
	beverages = itemsByCourse(restaurant_id, 'Beverage')
	return render_template('menu.html', restaurant = restaurant, appetizers = appetizers,
		entrees = entrees, desserts = desserts, beverages = beverages, items = items)

# Add a new menu item to an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = queryRestaurant(restaurant_id)
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'],
			course = request.form['course'], price = request.form['price'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash(newItem.name + " succesfully added to " + restaurant.name + "!")
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))
	else:
		return render_template('newmenuitem.html', restaurant = restaurant)

# Edit an existing menu item.
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = queryRestaurant(restaurant_id)
	item = queryItem(menu_id)
	if request.method == 'POST':
		item.name = request.form['name']
		item.description = request.form['description']
		item.course = request.form['course']
		item.price = request.form['price']
		session.commit()
		flash(item.name + " succesfully updated at " + restaurant.name + "!")
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))
	else:
		return render_template('editmenuitem.html', restaurant = restaurant, item = item)

# Detele an existing menu item.
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = queryRestaurant(restaurant_id)
	item = queryItem(menu_id)	
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash(item.name + " succesfully deleted from " + restaurant.name + "!")		
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))
	else:
		return render_template('deletemenuitem.html', restaurant = restaurant, item = item)

## API Endpoints.  ##

#  Query list of restaurants via API request. ##
@app.route('/restaurants/JSON/')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants = [r.serialize for r in restaurants])

# Query entire menu for a restaurant via API request.  ##
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = queryRestaurant(restaurant_id)
    items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    return jsonify(menuItems = [i.serialize for i in items])

# Query info for a single menu item via API request.
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id, MenuItem.id == menu_id).one()
    print item
    return jsonify(menuItem = item.serialize)

## End of API Endpoints. ##

## End of Web App Routes.  ##


if __name__ == '__main__':
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)