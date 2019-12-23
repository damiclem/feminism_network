# Module for handling twitter requests


# Dependencies
import requests
import json
from requests import get, post


# Twitter APIs handler
class TwitterAPI():

    # Class constructor
    def __init__(self):
        # Initialize object attributes
        self.base_url = 'https://api.twitter.com/'  # Twitter APIs base url
        self.access_token = None  # Access token used for authenticating

    # Define request sent from current object
    def request(self, req, url, *args, version='1.1/', **kwargs):
        args = list(arg for arg in args)
        # Build full url and add it to args
        args.insert(0, '{:s}{:s}{:s}'.format(self.base_url, version, url))
        # Case user is authenticated: make authenticated request
        if self.access_token is not None:
            # Add authentication headers
            kwargs.setdefault('headers', {})
            kwargs['headers']['Authorization'] = 'Bearer {:s}'.format(self.access_token)
        # Make request
        return req(*args, **kwargs)

    # Logging in current instance
    def login(self, api_key, api_secret_key):
        # Initialize access token
        self.access_token = access_token = None
        # Request access tokens using API key as user and secret key as password
        req = self.request(
            req=post, url='oauth2/token', version='',
            auth=(api_key, api_secret_key),
            data={'grant_type': 'client_credentials'}
        )
        # Get status code
        status_code = req.status_code
        # Check response status 200 (OK)
        if(status_code == 200):
            access_token = req.json().get('access_token', None)
        # Set access token
        self.access_token = access_token
        # Return access token along with status code
        return access_token, status_code

    # Make a request to standard search API
    def standard_search(self, query, geocode=None, lang=None, locale=None,
        result_type='mixed', count=15, until=None, since_id=None, max_id=None,
        include_entities=False):
        # Send request
        req = self.request(
            req=get, url='search/tweets.json',
            params={'q': ['{:s}:{:s}'.format(k, query[k]) for k in query.keys()]}
        )


# Begin unit testing
if __name__ == '__main__':

    # Import API app-only credentials (i.e. no user context)
    with open('auth.json', 'r') as auth_json:
        auth_dict = json.load(auth_json)
    # Save API client key and secret
    api_key = auth_dict['api_key']
    api_secret_key = auth_dict['api_secret_key']

    # Define new Twitter APIs handler
    twitter = TwitterAPI()

    # Attempt to login
    token, status = twitter.login(api_key, api_secret_key)
    # Debug
    print('Token {:s}'.format(token))
    print('Status {:d}'.format(status))
    # Test login status
    assert status == 200, 'Authentication went wrong'
    assert token is not None, 'No token has been retrieved'
