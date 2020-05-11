import os
import psycopg2
import bmemcached
from flask import Flask
from flask_cors import CORS
import googleapiclient.discovery

__all__ = ["cur", "app", "mc", "youtube", "images_list", "YOUTUBE_CHANNELS"]

DATABASE_URL = os.environ["DATABASE_URL"]
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
YOUTUBE_CHANNELS = os.environ["YOUTUBE_CHANNEL_IDS"].split(";")

conn = psycopg2.connect(DATABASE_URL)  # , sslmode="require")
cur = conn.cursor()

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

images_list = open("images.txt").read().splitlines()

mc = bmemcached.Client(
    os.environ.get("MEMCACHEDCLOUD_SERVERS").split(","),
    os.environ.get("MEMCACHEDCLOUD_USERNAME"),
    os.environ.get("MEMCACHEDCLOUD_PASSWORD"),
)

app = Flask(__name__)
cors = CORS(app)

# Init routes
from . import routes
