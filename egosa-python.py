# tweepy.org ドキュメントのHello Tweepy より
import tweepy
import json
from datetime import datetime


def getSearch():
    
    # consumer_key等はapps.twitter.comからとってきたものを使う
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    # public_tweets = api.home_timeline()
    today = datetime.today().strftime('%Y-%m-%d')
    print(today)

    for tweet in api.search(q='"合唱"', lang='ja', result_type='recent',count=10, until=today):
        print (tweet.created_at)


def main():
    getSearch()

if __name__ == "__main__":
    main()