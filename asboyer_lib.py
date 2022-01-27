import requests
import json

def get_new_post():
    with open(f'./blog.json', 'r') as json_file:
        posts = json.load(json_file)
    url = "https://asboyer.com/data/blog/posts.json"
    r = requests.get(url)
    current_posts = r.json()
    current_post_titles = []
    for title in current_posts:
        if current_posts[title]['live'] == True:
            current_post_titles.append(title)
    if posts['live_posts'] != current_post_titles:
        r =  list(set(current_post_titles) - set(posts['live_posts']))
        posts['live_posts'] = current_post_titles
        with open(f'./blog.json', 'w') as json_file: 
            json.dump(posts, json_file, indent=4)
        data = {}
        data['title'] = r[0]
        data['date'] = current_posts[r[0]]['date']
        data['subjects'] = current_posts[r[0]]['subjects']
        data['id'] = current_posts[r[0]]['id']
        data['img'] = current_posts[r[0]]['cover_img']
        return data
    return {}
