import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)  # , sslmode='require')
cur = conn.cursor()

print("Creating articles table...")
cur.execute(
    """
create table if not exists articles (
    id          serial not null,
    title       text not null,
    url         text not null
        constraint articles_pk
            primary key,
    date        text,
    image_url   text,
    site_name   text not null,
    site_url    text not null,
    author_name text, 
    author_url  text,
    description text
);"""
)

conn.commit()
cur.close()
conn.close()
