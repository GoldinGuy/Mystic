import os
import psycopg2
from flask import Flask
from flask_cors import CORS

__all__ = ["cur", "app"]

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)  # , sslmode="require")
cur = conn.cursor()

app = Flask(__name__)
cors = CORS(app)

# Init routes
from . import routes
