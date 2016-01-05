from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer  # takes advantage of
#base web server technology
import cgi #common gateway interface.

# give access to the restaurantmenu database.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # function that determines what do for GET requests.
        try:

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += 'Supported Restaurants: <br><br>'

                # query restaurant table and return all rows.  Then return the name
                # of each restaurant and add a line break '<br>''
                allRestaurants = session.query(Restaurant).order_by(Restaurant.id).all()
                for restaurant in allRestaurants:
                    output += '{}<br>'.format(restaurant.name)
                    print restaurant.name
                    output += '<a href = "/restaurants/{}/edit">Edit</a><br>'\
                        .format(restaurant.id)
                    output += '<a href = "/restaurants/{}/delete">Delete</a><br>'\
                        .format(restaurant.id)
                    output += '<br>'

                output += '<br>Don\'t see the restaurant you\'re looking for?<br> \
                    <a href = "/restaurants/new">Add a new restaurant here.</a>'

                output += '</body></html>'

                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += 'Please provide the restaurant info below to add it:<br>'

                # no action item is needed if staying at the same address.
                output += '<form method = "POST" enctype = "multipart/form-data"> \
                    <p>Restaurant Name: <input name = \
                    "newRestaurantName" type = "text" \
                    placeholder = "New Restaurant Name"> \
                    <input type = "submit" value = "Submit"></p></form>'
                output += '</body></html>'

                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter(
                    Restaurant.id == restaurantIDPath).one()
                existingRestaurantName = myRestaurantQuery.name

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = ''
                    output += 'Enter complete restaurant info below to revise entry.<br>'
                    output += '<h3>Current Restaurant Name: {} </h3>'.format(existingRestaurantName)
                    output += '<form method = "POST" enctype = "multipart/form-data"> \
                        <p>New Restaurant Name: <input name = "updatedRestaurantName" type = \
                        "text" placeholder = "New Restaurant Name"><br><br><input type = "submit" \
                        value = "Submit"></p></form>'
                    output += '</body></html>'

                    self.wfile.write(output)
                    return

            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter(
                    Restaurant.id == restaurantIDPath).one()

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = ''
                    output += '<html><body>'
                    output += '<h3>Are you sure you want to delete {}?  This cannot be undone.</h3><br>'\
                        .format(myRestaurantQuery.name)
                    output += '<form method = "POST" enctype = "multipart/form-data"> \
                        <input type = "submit" value = "Delete"></p></form>'
                    output += '</body></html>'

                    self.wfile.write(output)
                    return

            if self.path.endswith('/underconstruction'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += "This part of the site is under construction.  Please \
                    click <a href = '/restaurants'>here</a> to return to the starting page."
                output += '</body></html>'

                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found {1}".format(self.path))

    def do_POST(self):

        try:
            if self.path.endswith('restaurants/new'):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type')) #parses into a main value and dictionary of parameters.

                if ctype == 'multipart/form-data':  # check to see if form data is being received.
                    fields = cgi.parse_multipart(self.rfile, pdict) # collect all of the fields in a form.
                    messagecontent = fields.get('newRestaurantName') # take out specific fields and store them in an array.  Each form item is returned as part of a list.

                # create a new object
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                output = ''
                output += '<html><body>'
                output += messagecontent[0] + ' has been added.<br> \
                    <a href = "/restaurants">Return to restaurants page.</a>'
                output += '</body></html>'

                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2]

                myRestaurantQuery = session.query(Restaurant).filter(
                    Restaurant.id == restaurantIDPath).one()

                existingRestaurantName = myRestaurantQuery.name

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newName = fields.get('updatedRestaurantName')

                    print existingRestaurantName
                    print newName[0]

                    updateRestaurant = session.query(Restaurant).filter(Restaurant.id \
                        == restaurantIDPath).one()
                    updateRestaurant.name = newName[0]
                    session.add(updateRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.end_headers()

                    output = ''
                    output += '<html><body>'
                    output += '{0} has been changed to {1}.'.format(
                        existingRestaurantName, updateRestaurant.name)
                    output += '<br><a href = "/restaurants">Return to Restaurants page.</a>'
                    output += '</body></html>'

                    self.wfile.write(output)
                    return

            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split('/')[2]

                myRestaurantQuery = session.query(Restaurant).filter(
                    Restaurant.id == restaurantIDPath).one()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    session.delete(myRestaurantQuery)
                    session.commit()

                    output = ''
                    output += '<html><body>'
                    output += '{} succesfully deleted.'.format(myRestaurantQuery.name)
                    output += '</body></html>'

                    self.wfile.write(output)
                    return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port {0}'.format(port)
        server.serve_forever()

    except KeyboardInterrupt:  # KeyboardInterrupt is a built in function in python.
    # Occurs when user holds control + c.
        print '^C entered, stopping web server...'
        server.socket.close()

if __name__ == '__main__':
    main()
