from flask_cors import CORS
from flask import Flask
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
    return json.dumps(retrieve_articles())


def retrieve_articles(count=10):
    cur.execute("SELECT * FROM articles ORDER BY date DESC LIMIT 50;")

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
