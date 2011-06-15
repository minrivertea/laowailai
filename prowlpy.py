__author__ = 'Jacob Burch'
__author_email__ = 'jacoburch@gmail.com'
__maintainer__ = 'Olivier Hervieu'
__maintainer_email__ = 'olivier.hervieu@gmail.com'
__version__ = 0.42

from httplib import HTTPSConnection as Https
from urllib import urlencode

API_DOMAIN = 'prowl.weks.net'

class Prowl(object):
    def __init__(self, apikey, providerkey = None):
        """
Initialize a Prowl instance.
"""
        self.apikey = apikey
       
        # Set User-Agent
        self.headers = {'User-Agent': "Prowlpy/%s" % str(__version__),
                        'Content-type': "application/x-www-form-urlencoded"}

        # Aliasing
        self.add = self.post
        
    def post( self, application=None, event=None,
                description=None,priority=0, providerkey = None):
        """
Post a notification..
You must provide either event or description or both.
The parameters are :
- application ; The name of your application or the application
generating the event.
- providerkey (optional) : your provider API key.
Only necessary if you have been whitelisted.
- priority (optional) : default value of 0 if not provided.
An integer value ranging [-2, 2] representing:
-2. Very Low
-1. Moderate
0. Normal
1. High
2. Emergency (note : emergency priority messages may bypass
quiet hours according to the user's settings)
- event : the name of the event or subject of the notification.
- description : a description of the event, generally terse.
"""

        # Create the http object
        h = Https(API_DOMAIN)
        
        # Perform the request and get the response headers and content
        data = {
            'apikey': self.apikey,
            'application': application,
            'event': event,
            'description': description,
            'priority': priority
        }

        if providerkey is not None:
            data['providerkey'] = providerkey

        h.request( "POST",
                    "/publicapi/add",
                    headers = self.headers,
                    body = urlencode(data))
        response = h.getresponse()
        request_status = response.status

        if request_status == 200:
            return True
        elif request_status == 401:
            raise Exception("Auth Failed: %s" % response.reason)
        else:
            raise Exception("Failed")
        
    def verify_key(self, providerkey = None):
        """
Verify if the API key is valid.
The parameters are :
- providerkey (optional) : your provider API key.
Only necessary if you have been whitelisted.
"""
        h = Https(API_DOMAIN)

        data = {'apikey' : self.apikey}

        if providerkey is not None:
            data['providerkey'] = providerkey

        h.request( "GET",
                    "/publicapi/verify"+ urlencode(data),
                    headers=self.headers)

        request_status = h.getresponse().status

        if request_status != 200:
            raise Exception("Invalid API Key %s" % self.apikey)