# Bing Wallpaper API
# References:
# https://github.com/zenghongtu/bing-wallpaper/blob/main/src/app.ts
# https://github.com/TimothyYe/bing-wallpaper/blob/master/wallpaper.go
# https://github.com/SerinaNya/Bing-Api/blob/master/index.php
import random

import flask
import requests

app = flask.Flask(__name__)

resolutions = [
    "UHD",
    "1920x1200",
    "1920x1080",
    "1366x768",
    "1280x768",
    "1024x768",
    "800x600",
    "800x480",
    "768x1280",
    "720x1280",
    "640x480",
    "480x800",
    "400x240",
    "320x240",
    "240x320",
]

markets = [
    "en-US",
    "zh-CN",
    "ja-JP",
    "en-AU",
    "en-GB",
    "de-DE",
    "en-NZ",
    "en-CA",
    "en-IN",
    "fr-FR",
    "fr-CA",
]

formats = ["xml", "js", "rss"]

endpoint = (
    "https://www.bing.com/HPImageArchive.aspx?format=js&idx={day}&n=1&mkt={market}"
)

wallpaperURL = "https://www.bing.com{urlbase}_{resolution}.jpg"


def get_urlbase(day="0", market="en-US"):
    url = endpoint.format(day=day, market=market)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["images"][0]["urlbase"]


def get_wallpaperURL(urlbase, resolution="UHD"):
    url = wallpaperURL.format(urlbase=urlbase, resolution=resolution)
    return url


def get(day=-1, resolution="UHD", market="en-US"):
    if (
        not (int(day) >= -1 and int(day) <= 7)
        or resolution not in resolutions
        or market not in markets
    ):
        raise ValueError("Bad arguments for Bing Wallpaper.")

    urlbase = get_urlbase(str(day), market)
    url = get_wallpaperURL(urlbase, resolution)
    return url


def response():
    # Get args from request
    day = flask.request.args.get("day", default=-1)
    resolution = flask.request.args.get("resolution", default="UHD")
    market = flask.request.args.get("market", default="en-US")
    # If day = random
    if day == "random":
        day = random.randint(0, 7)
    # If market = random
    if market == "random":
        market = random.choice(markets)
    # Get url
    url = get(day, resolution, market)
    # Return redirect
    return flask.redirect(url, code=302)


if __name__ == "__main__":
    app.add_url_rule("/", view_func=response)
    app.run(debug=True)
