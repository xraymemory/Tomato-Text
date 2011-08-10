#Michael Anzuoni
#<ma2161@bard.edu>
#May 13 2011


import cherrypy
import wsgiref.handlers
from rottentomatoes import RT
from rottentomatoes import rottentomatoes_api_key

class rottenResponse(object):

    #the index() function is run whenever someone texts the twilio num
    def index(self, Body="?", **kwargs):
        rt = RT(API_KEY) #API Key given to me by RottenTomatoes.com
		''' the & operator allows users to search for multiple movies in one text '''
        if '&' in Body:
            combinedRatings = ''
            titles = Body.split('&')
            for n in range(len(titles)):
                results = rt.search(titles[n])
                rating = results[0]['ratings']['critics_score']
                combinedRatings = combinedRatings + ' ' + str(rating)
            return self.text(combinedRatings)

        else:
            results = rt.search(Body)
            ''' The rottentomatoes api presents search results as a huge
                list, so this rating assignment parses through it and
                gets the first result. '''
            rating = results[0]['ratings']['critics_score']
            return self.text(str(rating)) #rating needs to be a string otherwise
                                          #trim() returns an error

    #sends the text to the user phone
    def text(self, response):
        s = """<?xml version="1.0" encoding="UTF-8" ?>
<Response>
    <Sms>%s</Sms>
</Response>
""" % (self.trim(response))
        return s

    #although the ratings are only 1-2 chars, it doesn't hurt
    #to make sure the text we are sending is less than 160 chars
    #because otherwise Twilios will refuse to send the text
    def trim(self, s):
        return s[0:160]

    #allows cherrypy to access the functions
    index.exposed = True

#initialize cherrypy for use in the google app engine
#app = cherrypy.tree.mount(rottenResponse(), "/")
#wsgiref.handlers.CGIHandler().run(app)

#initializes file for offline use
app = cherrypy.tree.mount(rottenResponse(), "/")
cherrypy.quickstart(app)
