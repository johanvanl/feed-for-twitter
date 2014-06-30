import webapp2
import cgi

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('index.html', 'r').read())

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
