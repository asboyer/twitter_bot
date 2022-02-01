import time
import twitter_lib

while True:
    try:
        twitter_lib.new_blog_post()
    except:
        pass
    twitter_lib.git_asboyer()
    time.sleep(3600)