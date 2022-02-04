import time
import twitter_lib

while True:
    try:
        twitter_lib.new_blog_post()
    except:
        pass
    # twitter_lib.git_asboyer()
    time.sleep(2)

    # idea to get around the github overtime error
    # see if there are changes and then check for commits