from typing import List, Dict
from datetime import datetime
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import logging
import os

from .scrapers import ALL_SCRAPERS, ScraperBase
from .scrapers.types import Article


class Scraper:
    db_conn: psycopg2.extensions.connection
    db_cur: psycopg2.extensions.cursor
    logger: logging.Logger

    scrapers: List[ScraperBase] = []

    def __init__(self, database_url: str):
        self.logger = logging.getLogger("scraper")

        self.db_conn = psycopg2.connect(database_url)
        self.db_cur = self.db_conn.cursor()

        self.logger.debug("Connected to db")

        for scraper in ALL_SCRAPERS:
            self.scrapers.append(scraper())

    def run(self):
        """
        Run the scraper.

        This will continuously check sites and update the database
        """

        articles = []
        for scraper in self.scrapers:
            articles.extend(scraper.scrape_articles())

        print("Collected {} articles:".format(len(articles)))
        for article in articles:
            print("#", article.title)
            print("  url    =", article.url)
            print("  image  =", article.image_url)
            print("  author = {} ({})".format(article.author_name, article.author_url))
            print("  date   =", article.date)
            print("  site   = {} ({})".format(article.site_name, article.site_url))
            print()

        if os.environ.get("MYSTIC_WRITE_TO_DB") is not None:
            self.insert_articles(articles)

    def insert_articles(self, articles: List[Article]):
        psycopg2.extras.execute_batch(
            self.db_cur,
            "insert into articles values (%s, %s, %s, %s, %s, %s, %s, %s) on conflict do nothing",
            [i.as_tuple() for i in articles],
        )
        self.db_conn.commit()

    def last_date_for_sites(self) -> Dict[str, datetime]:
        self.db_cur.execute(
            "SELECT DISTINCT ON (site_name) site_name, date FROM articles ORDER BY site_name, date DESC"
        )
        results = self.db_cur.fetchall()
        return dict(map(lambda x: (x[0], datetime.fromisoformat(x[1])), results))
