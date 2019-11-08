import os
import tweepy

def tweepy_authorization():
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY')
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET')
    access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    # consumer_key等はapps.twitter.comからとってきたものを使う
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    return tweepy.API(auth)