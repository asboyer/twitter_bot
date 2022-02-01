from github import Github
from secret import gh_access_token
import pytz
from datetime import datetime, timezone
import json

git = Github(gh_access_token)

def get_latest_commit():
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
    dic['date'] = date.strftime(fmt + " %p")
    dic['message'] = message
    dic['url'] = url

    return dic
