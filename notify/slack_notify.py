import os
import json, requests



urls = os.environ.get('SLACK_NOTIFY_URLS')
url_list = urls.split()

def notification_twitter_to_slack(tweet):
    text = "*SNS* :Twitter\n"
    text += "*ユーザー名* :" + tweet.user.name + "\n"
    text += "*投稿時間* :" + tweet.created_at.strftime('%Y-%m-%d %H:%M:%S') + "\n"
    text += "*本文* :\n" + tweet.text + "\n"
    text += "*URL* :\n https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str

    # url_listに格納されているWebhook URLごとに通知をポスト
    for url in url_list:
        requests.post(url, data=json.dumps({
            "blocks": [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                },
                "accessory": {
                    "type": "image",
                    "image_url": tweet.user.profile_image_url,
                    "alt_text": "profile_image"
                }
            }]
        }))

