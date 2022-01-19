import tweepy
import secret
import os
from tweepy import OAuthHandler

auth = OAuthHandler(secret.consumer_key, secret.consumer_secret)
auth.set_access_token(secret.access_token, secret.access_token_secret)

api = tweepy.API(auth)
api.verify_credentials()

for tweet in tweepy.Cursor(api.search_tweets, q='asboyer.com').items():
   print(tweet.user.name)
