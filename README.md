# egosa-twitter-python

# 使用プロダクト
- CloudRun
- Firestore
    - 最後に取得したツイート、投稿のみレコードとして保存
    - 次回処理時に上記を読み込んでdiffを取る

# 起動方法
- Dockerをインストール
- docker build -t cancaonova-egosa .
- docker run -itd -e PORT=8000 -e GLOBAL_WORD=<全体検索をしたいワード> -e TIMELINE_WORD=<自分のフォロワーのつぶやき中で検索したいワード> -e TWITTER_CONSUMER_KEY=<Twitterのコンシューマキー> -e TWITTER_CONSUMER_SECRET=<Twitterのコンシューマシークレット> -e TWITTER_ACCESS_TOKEN=<Twitterのアクセストークン> -e TWITTER_ACCESS_TOKEN_SECRET=<Twitterのアクセストークンシークレット>  -e USER_NAME=<使用ユーザー名(Firestoreレコードのprefixになる)> -e FIREBASE_CREDENTIAL=<Firestoreのクレデンシャル情報のパス> -e SLACK_NOTIFY_URLS=<SlackのWebhookアドレス(アプリ版)> -e EXCLUSION_USER=<検索から除外したいユーザーのID(@は外す)> -p 8000:8000 cancaonova-egosa:latest
- docker exec -i -t コンテナ名 bash

# デプロイ
- Container Registoryに配置
  - gcloud builds submit --tag gcr.io/<GCPプロジェクトID>/cancaonova-egosa
- CloudRunにデプロイ
- CloudRunの環境変数セット
  - gcloud beta run services update <サービス名> --update-env-vars GLOBAL_WORD='',TIMELINE_WORD='',TWITTER_CONSUMER_KEY="",TWITTER_CONSUMER_SECRET="",TWITTER_ACCESS_TOKEN="",TWITTER_ACCESS_TOKEN_SECRET="",USER_NAME="",FIREBASE_CREDENTIAL="",SLACK_NOTIFY_URLS="",EXCLUSION_USER=""

# 注意
- ワードやユーザーなどを複数指定したい場合は半角スペースを入れる
- Ex. 
```
docker run -itd -e PORT=8000 -e GLOBAL_WORD='カンサォン カンサォン・ノーヴァ カンサォンノーヴァ' -e TIMELINE_WORD='ノーヴァ カンサォン カンサォン・ノーヴァ ' -e TWITTER_CONSUMER_KEY="xxxxx" -e TWITTER_CONSUMER_SECRET="xxxxx" -e TWITTER_ACCESS_TOKEN="xxxxx" -e TWITTER_ACCESS_TOKEN_SECRET="xxxxx" -e USER_NAME="nova" -e FIREBASE_CREDENTIAL="./xxxxxxxx.json" -e SLACK_NOTIFY_URLS="https://hooks.slack.com/xxxxxxxx https://hooks.slack.com/yyyyyy" -e EXCLUSION_USER="" -p 8000:8000 cancaonova-egosa:latest
```