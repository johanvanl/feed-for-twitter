import webapp2
import cgi

#import urllib

# import xml.etree.ElementTree as ET

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('index.html', 'r').read())

class Timeline(webapp2.RequestHandler):
    def get(self, twitter_handle):
        url = 'http://twitter.com/' + twitter_handle
        html = urllib.urlopen(url).read()
        self.response.write(html)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/(\w+)', Timeline)
], debug=True)

def main():
  from paste import httpserver
  httpserver.serve(application, host='127.0.0.1', port='8080')

if __name__ == '__main__':
  main()
