import tweepy
import secret
import os

auth = tweepy.OAuthHandler(secret.consumer_key, secret.consumer_secret)
auth.set_access_token(secret.access_token, secret.access_token_secret)

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.user_timeline).items():
    print(os.get_terminal_size().columns * "*")
    print(tweet.text)