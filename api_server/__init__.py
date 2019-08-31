from flask_cors import CORS
from flask import Flask
from flask import request
import json
import psycopg2
import os


DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)  # , sslmode="require")
cur = conn.cursor()

app = Flask(__name__)
cors = CORS(app)


@app.route("/articles")
def articles():
    page = int(request.args.get("page", 0))
    return json.dumps(retrieve_articles(page=page))


@app.route("/articles/by/<site>")
def articles_by_site(site):
    page = int(request.args.get("page", 0))
    return json.dumps(retrieve_articles_from(site, page=page))


def retrieve_articles_from(site, count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url "
        "FROM articles WHERE LOWER(site_name) = %s ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (site.lower(), count, page * count),
    )

    return fetch_requested_articles()


def retrieve_articles(count=50, page=0):
    cur.execute(
        "SELECT title, url, date, image_url, site_name, site_url, author_name, author_url "
        "FROM articles ORDER BY date DESC, id ASC LIMIT %s OFFSET %s;",
        (count, page * count),
    )
    return fetch_requested_articles()


def fetch_requested_articles():
    output = []
    for article in cur.fetchall():
        output.append(
            {
                "title": article[0],
                "url": article[1],
                "date": article[2],
                "image_url": article[3],
                "site_name": article[4],
                "site_url": article[5],
                "author_name": article[6],
                "author_url": article[7],
            }
        )
    return output


if __name__ == "__main__":
    app.run()
