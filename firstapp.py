from flask import Flask
from flask import render_template
from flask import request
import feedparser

app = Flask(__name__)

RSS_FEEDS={
    'toi': "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
    'fox': "http://feeds.foxnews.com/foxnews/latest"
}

@app.route("/")
def get_news():

    query = request.args.get("publication") # .get() is [], nut handles exceptions
    if not query or query.lower() not in RSS_FEEDS:
        publication = "toi"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template("home.html",articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)