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

BEARER_TOKEN = secret.bearer_token

# its bad practice to place your bearer token directly into the script (this is just done for illustration purposes)
# define search twitter function
def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    # print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#search term
query = "asboyer.com"
#twitter fields to be returned by api call
tweet_fields = "tweet.fields=text,author_id,created_at"

#twitter api call
json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)
#pretty printing
tweets = json_response['data']
for t in tweets:
    # print(t)
    # if t['id'] in data['ids']:
    #     continue
    username = api.get_user(user_id=t['author_id']).screen_name
    print(username)
#     reply_id = api.update_status(status=f'@{username} congrats! you found the best website of all time!', in_reply_to_status_id=t['id'], auto_populate_reply_metadata=True).id_str
#     data['ids'].append(t['id'])
#     data['reply_ids'].append(reply_id)
#     data['num'] += 1
#     data['author_ids'].append(t['author_id'])
    if data['most_popular_author'] == '':
        data['most_popular_author'] = username
    else:
        m_id = api.get_user(screen_name=data['most_popular_author']).id_str
        m = api.get_user(user_id=m_id).followers_count
        for author in data['author_ids']:        
            n = api.get_user(user_id=author).followers_count
            if n > m:
                m = n
                m_id = author
        data['most_popular_author'] = api.get_user(user_id=m_id).screen_name

print(data['most_popular_author'])
print(api.get_user(screen_name=data['most_popular_author']).followers_count)
# with open(f'./tweets.json', 'w') as json_file: 
#     json.dump(data, json_file, indent=4)
