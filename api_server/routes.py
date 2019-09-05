from flask import request
import json

from . import backend
from . import app


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
    return json.dumps({"url": backend.fetch_scryfall_latest_promo()})
