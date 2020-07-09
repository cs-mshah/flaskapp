import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import feedparser
import json
import urllib.parse
from urllib.request import urlopen

app = Flask(__name__)

#-------GLOBAL VARIABLES--------------------
RSS_FEEDS={
    'toi': "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    'bbc': "http://feeds.bbci.co.uk/news/rss.xml",
    'fox': "http://feeds.foxnews.com/foxnews/latest"
}

DEFAULTS = {'publication':'toi','city':'Pune,India','currency_from':'USD','currency_to':'INR'}

WEATHER_URL="https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=b288333a499478e32d80beb4e5587800"
CURRENCY_URL ="https://openexchangerates.org//api/latest.json?app_id=33e74ac1adb342afbed9954dbb011f9b"
#-------GLOBAL VARIABLES END--------------------

def get_value_with_fallback(key):

    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key): # cookies
        return request.cookies.get(key)
    else:
        return DEFAULTS.get(key)

@app.route("/")
def home():

    # get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)


    #COOKIES
    response = make_response(render_template("home.html",
        articles=articles,
        weather=weather,
        currency_from=currency_from,
        currency_to=currency_to,
        rate=rate,
        currencies=sorted(currencies)))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from",currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response # use cookies
    #return render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate,currencies=sorted(currencies))

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