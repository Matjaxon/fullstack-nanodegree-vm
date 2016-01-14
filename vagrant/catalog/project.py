from flask import Flask, render_template, url_for, request #reqeust lets us get info from forms
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

# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(menuItems = [i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    print item
    return jsonify(menuItem = item.serialize)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

    # Rather than writing out each output we leverage the render template which
    # already has the formatting and the python code for structuring the output.
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
# By adding the methods argument to the route decorator you can make it repsond
# to more than just GET requests.
def newMenuItem(restaurant_id):
    if request.method == 'POST':  # Looks for a POST request.
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem) # Adds new item to database
        session.commit() # Commit new item to database
        flash("New item created!")

        # Redirect back to restaurantMenu page after new item is committed.
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        
        # If you have not submitted a POST request then render the page to allow you
        # to submit a new menu item.
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, 
        id = menu_id).one()   
    if request.method == 'POST': # Looks for a POST request.
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Item successfully edited!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, 
            menu_id = menu_id, i = editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, 
        id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Item successfully deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, 
            menu_id = menu_id, i = deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # creates user specific sessions of a website.  Should have a very secure password if live.
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
