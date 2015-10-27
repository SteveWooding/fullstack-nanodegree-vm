from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import cgi


def connect_to_db(dbname="sqlite:///restaurantmenu.db"):
    """Setup the connection to the database"""
    engine = create_engine("sqlite:///restaurantmenu.db")
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello!"
            message += ("<form method='POST' enctype='multipart/form-data' "
                        "action='/hello'><h2>What would you like me to say?"
                        "</h2><input name='message' type='text'><input type="
                        "'submit' value='Submit'></form>")
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += ("<html><body>&#161Hola! <a href='/hello'>Back to Hello"
                        "</a>")
            message += ("<form method='POST' enctype='multipart/form-data' "
                        "action='/hola'><h2>What would you like me to say?"
                        "</h2><input name='message' type='text'><input type="
                        "'submit' value='Submit'></form>")
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/restaurants"):
            db_session = connect_to_db()
            restaurants = db_session.query(Restaurant).all()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += ("<html><body>")
            message += "<p><a href='/restaurants/new'>Make a New Restaurant Here</a></p>"

            for restaurant in restaurants:
                message += "<p>%s</br>" % restaurant.name
                message += "<a href='#'>Edit</a></br>"
                message += "<a href='#'>Delete</a></p>"

            message += ("</body></html>")
            self.wfile.write(message)
            print message
            return

        elif self.path.endswith("/restaurants/new"):
            db_session = connect_to_db()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body><h1>Make a New Restaurant</h1>"
            message += (
                "<form method='POST' enctype='multipart/form-data' "
                "action='/restaurants/new'><input name='rest_name' type='text' "
                "placeholder='New Restaurant Name'>"
                "<input type='submit' value='Create'></form>")

            message += ("</body></html>")
            self.wfile.write(message)
            print message

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_name = fields.get('rest_name')

                # Add the new restaurant to the database.
                db_session = connect_to_db()
                new_restaurant = Restaurant(name=restaurant_name[0])
                db_session.add(new_restaurant)
                db_session.commit()

                # Redirect to the restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return


            else:
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this:</h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += ("<form method='POST' enctype='multipart/form-data' "
                        "action='/hello'><h2>What would you like me to say?"
                        "</h2><input name='message' type='text'><input type="
                        "'submit' value='Submit'></form>")

                output += "</body></html>"
                self.wfile.write(output)
                print output

                return

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
