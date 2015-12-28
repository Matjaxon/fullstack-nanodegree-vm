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
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers() # Send a blank line.

                output = ''
                output += '<html><body>'
                output += 'Hello!'
                output += "<form method = 'POST' enctype = 'multipart/form-data' \
                action = 'hello'><h2>What would you like me to say?</h2><input name = \
                'message' type = 'text' ><input type = 'submit' value = 'Submit'></form>"
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return # Exit try function via a return

            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers() # Send a blank line.

                output = ''
                output += '<html><body>'
                output += '&#161 Hola ! <a href = "/hello" > Back to Hello</a>'
                output += "<form method = 'POST' enctype = 'multipart/form-data' \
                action = 'hello'><h2>What would you like me to say?</h2><input name = \
                'message' type = 'text' ><input type = 'submit' value = 'Submit'></form>"
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return # Exit try function via a return

            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += 'restaurants starter page'
                output += '</body></html>'

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found {1}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            # next, need to decipher the message that is received from the server.

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type')) #parses into a main value and dictionary of parameters.
            if ctype == 'multipart/form-data':  # check to see if form data is being received.
                fields = cgi.parse_multipart(self.rfile, pdict) # collect all of the fields in a form.
                messagecontent = fields.get('message') # take out specific fields and store them in an array.

            output = ''
            output += '<html><body>'
            output += ' <h2> Okay, how about this:  </h2>'
            output += ' <h1> {0} </h1>'.format(messagecontent[0])

            # need to create an html form to prompt the user for some data.
            output += "<form method = 'POST' enctype = 'multipart/form-data' \
            action = 'hello'><h2>What would you like me to say?</h2><input name = \
            'message' type = 'text' ><input type = 'submit' value = 'Submit'></form>"
            output += '</body></html>'
            self.wfile.write(output)
            print output  # printing out for debugging.

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
