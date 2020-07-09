from flask import Flask
from flask import render_template
import feedparser

app = Flask(__name__)

RSS_FEEDS={
    'toi': "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
    'fox': "http://feeds.foxnews.com/foxnews/latest"
}

@app.route("/")
@app.route("/<publication>")
def get_news(publication='toi'):

    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template("home.html",articles=feed['entries'])
if __name__ == "__main__":
    app.run(port=5000, debug=True)