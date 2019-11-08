import os
import tweepy
import json
from datetime import datetime
import lib.tweepy_auth as ta
import lib.firestore_auth as fa
import notify.slack_notify as slack_notify
import firebase_admin
import lib.util as util
from firebase_admin import credentials
from firebase_admin import firestore
from functools import reduce

db = fa.firestore_authorization()
api = ta.tweepy_authorization()
# 検索ワードをTwitterAPI用に加工
thread_keyword = os.environ.get('GLOBAL_WORD')
thread_query = ' OR '.join(thread_keyword.split()) + ' exclude:retweets'

exclusion_user = os.environ.get('EXCLUSION_USER').split()
if exclusion_user != "":
    for user in exclusion_user:
        thread_query += ' -from:'
        thread_query += user
        thread_query += ' -to:'
        thread_query += user

timeline_keyword = os.environ.get('TIMELINE_WORD')
timeline_keyword_list = timeline_keyword.split()
user_name = os.environ.get('USER_NAME')

print(thread_query)

def search_thread():
    # 初期実行かチェック
    last_tweet_id = check_record_empty('_thread_last_record')
    if last_tweet_id is None:
        return

    print(last_tweet_id)
    tweets = []
    # 最新ツイートから検索条件にヒットするものを取得
    for tweet in api.search(q=thread_query, lang='ja', result_type='recent',count=100):
        # 前回取得ツイート以前のものがある場合はfor文を抜ける
        if tweet.id <= last_tweet_id:
            break
        else:
            tweets.append(tweet)
            # slackへ通知
            slack_notify.notification_twitter_to_slack(tweet)

    if tweets:
        # 配列から一番新しいツイートを取得
        first_tweet = tweets[0]
    else:
        return

    # Firestoreのレコードを最新ツイートのIDに更新
    doc_ref = db.collection(u'twitter_ids').document(user_name+'_thread_last_record')
    doc_ref.set({
    u'tweet_id': first_tweet.id,
    u'timestamp': first_tweet.created_at
    })

def search_timeline():
    # 初期実行かチェック
    last_tweet_id = check_record_empty('_timeline_last_record')
    if last_tweet_id is None:
        return

    # print(last_tweet_id)
    tweets = []
    # 自分のタイムラインから200件取得
    for tweet in api.home_timeline(count=200):
        if tweet.id <= last_tweet_id:
            # 前回取得ツイート以前のものがある場合はfor文を抜ける
            break
        elif hasattr(tweet, 'retweeted_status'):
            # リツイートを除外
            continue
        elif util.search_or(timeline_keyword_list, tweet.text):
            tweets.append(tweet)
            # slackへ通知
            slack_notify.notification_twitter_to_slack(tweet)
        else:
            continue

    if tweets:
        # 配列から一番新しいツイートを取得
        first_tweet = tweets[0]
    else:
        return

    # Firestoreのレコードを最新ツイートのIDに更新
    doc_ref = db.collection(u'twitter_ids').document(user_name+'_timeline_last_record')
    doc_ref.set({
    u'tweet_id': first_tweet.id,
    u'timestamp': first_tweet.created_at
    })


# 初期実行か否かチェック、初期実行ならFirestoreにlast_recordを挿入
def check_record_empty(record_name):
    # Firestoreから前回実行時のTwitterIDを取得
    doc = db.collection(u'twitter_ids').document(user_name + record_name).get()
    try:
        # Firestoreからデータを取得できたかチェック
        last_tweet_id = doc.to_dict()[u'tweet_id']
        return last_tweet_id
    except:
        # Firestoreにデータがない(初期実行)のときのみ、1件取得してレコード更新し、終了
        tweets_for_init = api.search(q=thread_query, lang='ja', result_type='recent',count=200)
        doc_ref = db.collection(u'twitter_ids').document(user_name + record_name)
        doc_ref.set({
        u'tweet_id': tweets_for_init[0].id,
        u'timestamp': tweets_for_init[0].created_at
        })
        return None