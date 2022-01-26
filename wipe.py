import tweepy
import secret
import os
from tweepy import OAuthHandler
import requests
import json

with open(f'./tweets.json', 'r') as json_file:
    data = json.load(json_file)

auth = OAuthHandler(secret.consumer_key, secret.consumer_secret)
auth.set_access_token(secret.access_token, secret.access_token_secret)

api = tweepy.API(auth)
api.verify_credentials()

for i_d in data['reply_ids']:
    api.destroy_status(i_d)

# delete all tweets in data
# revert data back to normal
data['ids'] = []
data['reply_ids'] = []
data['num'] = 0
data['author_ids'] = []
data['most_popular_author'] = ''

with open(f'./tweets.json', 'w') as json_file: 
    json.dump(data, json_file, indent=4)
