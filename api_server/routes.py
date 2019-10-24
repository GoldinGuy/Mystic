from flask import request
import json
import random

from . import backend
from . import app
from . import images_list


@app.route("/articles")
def articles():
    page = int(request.args.get("page", 0))
    return json.dumps(backend.retrieve_articles(page=page))


@app.route("/articles/by")
def articles_by_multiple_sites():
    page = int(request.args.get("page", 0))
    sites = request.args.getlist("site")
    if len(sites) == 0:
        return "{}"
    return json.dumps(backend.retrieve_articles_from_multiple(tuple(sites), page=page))


@app.route("/articles/by/<site>")
def articles_by_site(site):
    page = int(request.args.get("page", 0))
    return json.dumps(backend.retrieve_articles_from(site, page=page))


@app.route("/scryfall-promo-set")
def scryfall_promo_set():
    return json.dumps(backend.fetch_scryfall_latest_promo())


@app.route("/videos")
def videos():
    page_token = request.args.get("page_token")
    return json.dumps(backend.fetch_youtube_uploads(page_token))


@app.route("/random_art")
def random_art():
    count = int(request.args.get("count", 1))
    count = min(count, 100)
    return json.dumps(
        list(
            map(
                lambda c: "https://img.scryfall.com/cards/art_crop/front/" + c,
                random.choices(images_list, k=count),
            )
        )
    )
