from flask import Flask
from flask import render_template
from flask import request
import feedparser
import json
import urllib.parse
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS={
    'toi': "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
    'fox': "http://feeds.foxnews.com/foxnews/latest"
}

DEFAULTS = {'publication':'toi','city':'London,UK','currency_from':'USD','currency_to':'INR'}

WEATHER_URL="https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=b288333a499478e32d80beb4e5587800"
CURRENCY_URL ="https://openexchangerates.org//api/latest.json?app_id=33e74ac1adb342afbed9954dbb011f9b"


@app.route("/")
def home():

    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate,currencies=sorted(currencies))

def get_news(query):

    # .get() is [], but handles exceptions
    if not query or query.lower() not in RSS_FEEDS:
        publication = "toi"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']

def get_weather(query):

    the_query = urllib.parse.quote(query)
    url = WEATHER_URL.format(the_query)

    data = urlopen(url).read()

    parsed = json.loads(data)

    weather = None

    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                "temperature":parsed["main"]["temp"],
                "city":parsed["name"]
                }

    return weather

def get_rate(frm, to):

    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')

    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return (to_rate/frm_rate,parsed.keys())

if __name__ == "__main__":
    app.run(port=5000, debug=True)