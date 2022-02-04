import time
import twitter_lib

while True:
    twitter_lib.reply_bot()
    try:
        twitter_lib.new_blog_post()
    except:
        pass
    time.sleep(2)