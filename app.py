import os
import sns_search.twitter_egosa as twitter
from flask import Flask

app = Flask(__name__)

@app.route('/')
def egosa():
    twitter.search_thread()
    twitter.search_timeline()
    return "success"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))