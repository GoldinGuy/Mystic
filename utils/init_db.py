import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)  # , sslmode='require')
cur = conn.cursor()

print("Creating articles table...")
cur.execute(
    """
create table if not exists articles (
    title        text not null,
    url          text not null,
    date         text,
    image_url    text,
    site_name    text not null,
    site_url     text not null,
    author_name  text not null,
    author_url   text
);"""
)

conn.commit()
cur.close()
conn.close()
