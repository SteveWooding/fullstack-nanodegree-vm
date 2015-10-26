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
                        "action='/hello'><h2>What would you like me to say?"
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

            for restaurant in restaurants:
                message += "<p>%s</p>" % restaurant.name

            message += ("</body></html>")
            self.wfile.write(message)
            print message
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
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
