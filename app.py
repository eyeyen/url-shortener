import random
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

"""
Intro:
    Basic URL Shortener
Author:
    Ian Blackman, 2021

Description:
    This application is a proof of concept of a URL Shortener Service

API:
    METHOD  ENDPOINT        RESPONSE
    GET     /urls           All URLs
    GET     /url/<ID>       Single url by ID
    GET     /url/<SHORT>    Redirect to original URL via Shortened URL
    POST    /urls           Create shortened URL with ID
    DELETE  /urls/<ID>      Remove URL, returns 200 OK

TODO:
    0. Script test cases
    1. Connect to database
    2. Error checking
    3. PUT to update URL maybe
    4. Custom URLs?
    5. Check URL already exists (de-dupe)
"""


# setup mock data
urls = [
    {"id": 1, "url": "https://unitedmasters.com/about", "short": "abtUM"},
    {"id": 2, "url": "https://store.google.com/US/?utm_source=hp_header&utm_medium=google_ooo&utm_campaign=GS100042&hl=en-US", "short": "ggLSt"},
    {"id": 3, "url": "https://en.wikipedia.org/wiki/URL_shortening", "short": "wksUL"},
]

def _get_next_id():
    return max(url["id"] for url in urls) + 1

def _gen_short_url(input_url):
    input_url = ''.join(e for e in input_url if e.isalnum())
    return ''.join(random.choice(input_url) for _ in range(5))

@app.get("/urls")
def get_urls():
    return jsonify(urls)

@app.get("/url/<int:url_id>")
def get_id_url(url_id):
    index = url_id -1
    if index in range(-len(urls), len(urls)):
        return urls[url_id-1]
    return {"error": "Index out of range"}, 415

@app.get("/url/<string:short_url>")
def get_url(short_url):
    for elem in urls:
        if short_url == elem["short"]:
            return redirect(elem["url"])
    return {"error": "Short URL not found"}, 415


"""
Expected input:
    '{"url":"http://some.url"}'
"""
@app.post("/urls")
def shorten_url():
    if request.is_json:
        url = request.get_json()
        url["id"] = _get_next_id()
        # can also give service option to do custom URLS
        url["short"] = _gen_short_url(url["url"])
        urls.append(url)
        return url, 201
    return {"error": "Request must be JSON"}, 415

@app.delete("/urls/<string:url>")
def remove_url(url):
    for elem in urls:
        if url == elem["short"]:
            urls.remove(elem)
            return {"success": "Removed"}, 200
    return {"error": "Short URL not found"}, 415
