#!/usr/bin/env python
# coding: utf-8

# # Twitter
# 
# Exploitation of twitter resources available from APIs. 

# In[ ]:


# Import libraries
import requests
import json


# In[ ]:


# Import API app-only credentials (i.e. no user context)
with open('auth.json', 'r') as auth_json:
    auth_dict = json.load(auth_json)
    
# Save API client key and access token
api_key = auth_dict['api_key']
api_secret_key = auth_dict['api_secret_key']
# access_token = auth_dict['access_token']
# access_secret_token = auth_dict['access_secret_token']
print(api_key)
print(api_secret_key)


# In[ ]:


# Request access tokens using API key as user and secret key as password
r = requests.post(
    'https://api.twitter.com/oauth2/token', 
    auth=(api_key, api_secret_key),
    data={'grant_type': 'client_credentials'}
)

# Show request result
print('Authentication returned status {:d}'.format(r.status_code))

# Save access token
access_token = r.json().get('access_token', None)
assert access_token is not None  # Check access


# ## Getting user's timeline

# In[ ]:


# Request lat and long for 'Padova' city
r = requests.get(
    'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=BarackObama&count=10',
    headers={'Authorization': 'Bearer {:s}'.format(access_token)}
)

# Show response
r.json()


# In[ ]:


# Get all returned tweets
tweets = r.json()

# Get last returned tweet (in ascending temporal order)
tweet = tweets[0]
print(tweet.get('created_at'))  # Print date and time
print(tweet.get('user').get('name'), tweet.get('user').get('location'))  # Print user name and location
print(tweet.get('text'))  # Print tweet text


# ## Getting location (global) trends

# In[ ]:


# Request lat and long for 'Padova' city
r = requests.get(
    'https://api.twitter.com/1.1/trends/place.json?id=1',
    headers={'Authorization': 'Bearer {:s}'.format(access_token)}
)

# Show response
r.json()


# In[ ]:


# Get trends list
trends = r.json()[0]['trends']

# Show 10 trending topics, worldwide
print('Worldwide trending topics:')
for trend in trends[:10]:
    name = trend.get('name')
    volume = trend.get('tweet_volume')
    print('  {} tweeted {} times'.format(name, volume))


# In[ ]:




