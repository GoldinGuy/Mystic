import os
import psycopg2
import bmemcached
from flask import Flask
from flask_cors import CORS

__all__ = ["cur", "app", "mc"]

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)  # , sslmode="require")
cur = conn.cursor()

mc = bmemcached.Client(
    os.environ.get("MEMCACHEDCLOUD_SERVERS").split(","),
    os.environ.get("MEMCACHEDCLOUD_USERNAME"),
    os.environ.get("MEMCACHEDCLOUD_PASSWORD"),
)

app = Flask(__name__)
cors = CORS(app)

# Init routes
from . import routes
