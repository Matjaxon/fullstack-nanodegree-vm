from flask import Flask
from flask import render_template
from flask import url_for


app = Flask(__name__)


# FAKE Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

# FAKE Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

# See all restaurants.
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	# return "This page will show all my restaurants"
	return render_template('restaurants.html', restaurants = restaurants)

# Create a new restaurant.
@app.route('/restaurants/new/')
def newRestaurant():
	# return "This page will be for making a new restaurant."
	return render_template('newrestaurant.html', restaurant = restaurant)

# Edit an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
	# return "This page will be for editing restaurant {0}".format(restaurant_id)
	return render_template('editrestaurant.html', restaurant = restaurant)

# Delete an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
	# return "This page will be for deleting restaurant {0}".format(restaurant_id)
	return render_template('deleterestaurant.html', restaurant = restaurant)

# Show the menu for a given restaurant.
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	# return "This page is the menu for restaurant {0}".format(restaurant_id)
	return render_template('menu.html', restaurant = restaurant)

# Add a new menu item to an existing restaurant.
@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
	# return 'This page is for making a new menu item for restaurant {0}'.format(restaurant_id)
	return render_template('newmenuitem.html', restaurant = restaurant)

# Edit an existing menu item.
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	# return 'This page is for editing item {0} at restaurant {1}'.format(menu_id, restaurant_id)
	return render_template('editmenuitem.html', restaurant = restaurant, menu_id = menu_id)

# Detele an existing menu item.
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	# return 'This page is for deteling item {0} at restaurant {1}'.format(restaurant_id, menu_id)
	return render_template('deletemenuitem.html', restaurant = restaurant, menu_id = menu_id)

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)