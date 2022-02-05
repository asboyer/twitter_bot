import time
import twitter_lib

while True:
    twitter_lib.reply_bot() 
    twitter_lib.git_asboyer()
    try:
        twitter_lib.new_blog_post()
    except:
        pass
    time.sleep(2)