import tweepy
import secret
import os
from tweepy import OAuthHandler
import requests
import json
import github_lib, asboyer_lib

auth = OAuthHandler(secret.consumer_key, secret.consumer_secret)
auth.set_access_token(secret.access_token, secret.access_token_secret)

api = tweepy.API(auth)
api.verify_credentials()

BEARER_TOKEN = secret.bearer_token

def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def reply_bot():
    with open(f'./tweets.json', 'r') as json_file:
        data = json.load(json_file)
    if data['latest_tweet_id'] == "":
        fields = "tweet.fields=text,author_id,created_at"
    else:
        fields = f"tweet.fields=text,author_id,created_at&since_id={data['latest_tweet_id']}"
    json_response = search_twitter(query="asboyer.com", tweet_fields=fields, bearer_token=BEARER_TOKEN)
    if json_response['meta']['result_count'] == 0:
        return
    tweets = json_response['data']
    latest = False
    for t in tweets:
        print(t)
        data['num'] += 1
        if t['author_id'] in data['author_ids'] or t['author_id'] == "1303670607759003649": 
            if not latest:
                data['latest_tweet_id'] = t['id']
                latest = True
            continue
        username = api.get_user(user_id=t['author_id']).screen_name
        reply_id = api.update_status(status=f'@{username} congrats! you found the best website of all time!', in_reply_to_status_id=t['id'], auto_populate_reply_metadata=True).id_str
        if not latest:
            data['latest_tweet_id'] = t['id']
            latest = True
        data['reply_ids'].append(reply_id)
        data['author_ids'].append(t['author_id'])
        data['author_ids'] = list(set(data['author_ids']))
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
            m_u = api.get_user(user_id=m_id).screen_name
            if m_u != data['most_popular_author']:
                so_id = api.update_status(status=f'@{username} is the most followed user on twitter who\'s talking about asboyer.com 🤫').id_str
                data["so_author_tweets"].append(so_id)
                data['most_popular_author'] = m_u
    with open(f'./tweets.json', 'w') as json_file: 
        json.dump(data, json_file, indent=4)

def wipe():
    with open(f'./tweets.json', 'r') as json_file:
        data = json.load(json_file)
    for i_d in data['reply_ids']:
        api.destroy_status(i_d)
    for so_id in data['so_author_tweets']:
        api.destroy_status(so_id)
    data['ids'] = []
    data['reply_ids'] = []
    data['num'] = 0
    data['author_ids'] = []
    data['most_popular_author'] = ''
    data['so_author_tweets'] = []
    data['latest_tweet_id'] = ''
    with open(f'./tweets.json', 'w') as json_file: 
        json.dump(data, json_file, indent=4)

def git_asboyer():
    latest_commit = github_lib.get_latest_commit()
    if latest_commit != {}:
        files_str = ""
        if len(latest_commit['files']) > 4:
            file_list = latest_commit['files'][0:5]
        else:
            file_list = latest_commit['files']
        for c in range(len(file_list)):
            files_str += f"- {file_list[c]}\n"
        status = f"""
asboyer.com has been updated!

date: {latest_commit['date']}
message: {latest_commit['message']}

a few files changed:
{files_str}

{latest_commit['url']}
        """
        print(status)
        api.update_status(status=status)
        

def new_blog_post():
    data = asboyer_lib.get_new_post()
    if data != {}:
        subject_str = ""
        for i in range(len(data['subjects'])):
            if i == len(data['subjects']) - 1:
                subject_str += data['subjects'][i]
            else:
                subject_str += data['subjects'][i] + ', '

        status = f"""
new asboyer.com blogpost!

asboyer.com/blog/{str(data['id'])}

title: {data['title']}
date: {data['date']}
subjects: {subject_str}
        """
        api.update_status(status=status)

# could add coming soon post
# see if there is a way to report data back
# manually wipe from somewhere
