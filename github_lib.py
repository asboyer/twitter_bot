import requests
from github import Github
from secret import gh_access_token
import pytz
from datetime import datetime, timezone
import json

def get_latest_commit():
    with open(f'./asboyer.json', 'r') as json_file:
        last_logged_commit = json.load(json_file)
    r = requests.get("https://github.com/asboyer/asboyer.com/commits/master")
    text = r.text
    commit_id = text.split("https://github.com/asboyer/asboyer.com/commit")[38][1:41]
    commit_url = f"https://github.com/asboyer/asboyer.com/commit/{commit_id}"
    if commit_url != last_logged_commit['url']:
        git = Github(gh_access_token)
        print('used github api')
        repo = git.get_repo("asboyer/asboyer.com")
        commits = repo.get_commits()
        while True:
            commit = list(commits)[0]
            if commit.commit.message.startswith('Merge branch \'master\''):
                commits = commits[1:]
            else:
                break
        files = commit.files
        file_list = []
        for f in files:
            names = f.filename.split('/')
            name = names[len(names) - 1]
            file_list.append(name)
        date = commit.commit.author.date
        message = commit.commit.message
        url = commit.html_url

        fmt = "%Y-%m-%d %I:%M:%S"
        date = datetime.fromisoformat(date.strftime(fmt)).replace(tzinfo=timezone.utc).astimezone(pytz.timezone("America/New_York"))

        dic = {}
        dic['files'] = file_list
        dic['date'] = date.strftime(fmt) + " " + datetime.now().strftime("%p")
        dic['message'] = message
        dic['url'] = url
        with open(f'./asboyer.json', 'w') as json_file: 
            json.dump(dic, json_file, indent=4)
        return dic
    return {}
