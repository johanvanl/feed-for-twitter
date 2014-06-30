import webapp2
import cgi

import urllib

import datetime

import xml.etree.ElementTree as ET
import bs4

# recursively get all the text in the structure and append them together
def getTweet(element):
    if type(element) is bs4.element.NavigableString:
        return element.encode('utf8')
    tweet = ""
    for e in element.contents:
        tweet += getTweet(e)
    return tweet

twitter_handle = 'cheese'

def getTweets(html):
    """
    Get the tweets from the html as a list of dictionaries.
    """
    soup = bs4.BeautifulSoup(html)
    li = soup.findAll('div',{'data-component-term':'tweet'})

    tweets = []
    for l in li:
        tweet = {}
        data = l.findAll('a',{'class':'ProfileTweet-timestamp js-permalink js-nav js-tooltip'})[0]
        tweet['guid'] = 'http://twitter.com' + data['href']
        tweet['link'] = 'http://twitter.com' + data['href']

        data = data.findAll('span')[0]
        tweet['pubDate'] = str(datetime.datetime.fromtimestamp(int(data['data-time'])))
        tweet['title'] = 'Tweet (' + tweet['pubDate'] + ')'

        data = l.findAll('p',{'class':'ProfileTweet-text js-tweet-text u-dir'})[0]
        tweet['description'] = getTweet(data)
    
        tweets.append(tweet)
        
    return tweets

def buildRSS(twitter_handle, tweets):
    rss = ET.Element('rss')
    channel = ET.SubElement(rss, 'channel')

    title = ET.SubElement(channel, 'title')
    title.text = 'Twitter timeline for @' + twitter_handle

    link = ET.SubElement(channel, 'link')
    link.text = 'http://twitter.com/' + twitter_handle

    for t in tweets:
        item = ET.SubElement(channel, 'item')

        title = ET.SubElement(item, 'title')
        title.text = t['title']

        description = ET.SubElement(item, 'description')
        description.text = t['description'].decode('utf8').replace('\n', ' ').replace('\r', '')

        link = ET.SubElement(item, 'link')
        link.text = t['link']

        guid = ET.SubElement(item, 'guid')
        guid.text = t['guid']

        pubDate = ET.SubElement(item, 'pubDate')
        pubDate.text = t['pubDate']

    return ET.tostring(rss, encoding='utf8', method='xml')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('index.html', 'r').read())

class Timeline(webapp2.RequestHandler):
    def get(self, twitter_handle):
        url = 'http://twitter.com/' + twitter_handle
        html = urllib.urlopen(url).read()
        tweets = getTweets(html)
        rss = buildRSS(twitter_handle, tweets)
        
        self.response.content_type = 'application/rss+xml'
        self.response.write(rss)

application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/(\w+)', Timeline)
], debug=True)

def main():
  from paste import httpserver
  httpserver.serve(application, host='127.0.0.1', port='8080')

if __name__ == '__main__':
  main()
