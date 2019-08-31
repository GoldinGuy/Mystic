import time
from typing import List, Dict
from datetime import datetime
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import dateparser
import logging
import os

from .scrapers import ALL_SCRAPERS, ScraperBase
from .scrapers.types import Article


class Scraper:
    db_conn: psycopg2.extensions.connection
    db_cur: psycopg2.extensions.cursor
    logger: logging.Logger

    scrapers: List[ScraperBase] = []
    # Delay between scrapes in minutes
    interval = 15

    def __init__(self, database_url: str):
        self.logger = logging.getLogger("scraper")

        self.db_conn = psycopg2.connect(database_url)
        self.db_cur = self.db_conn.cursor()

        self.logger.debug("Connected to db")

        interval = os.environ.get("MYSTIC_INTERVAL")
        if interval is not None:
            self.interval = int(interval)
        self.logger.info("Scraping interval set to {} minutes".format(self.interval))

        for scraper in ALL_SCRAPERS:
            self.scrapers.append(scraper())

    def run(self):
        """
        Run the scraper.

        This will continuously check sites and update the database
        """

        while True:
            self.logger.info("Scraping sites...")
            last_dates = self.last_date_for_sites()
            articles = []
            for scraper in self.scrapers:
                last_date = last_dates.get(scraper.SITE_NAME)
                if last_date is None:
                    last_date = dateparser.parse("1 week ago")

                articles.extend(scraper.scrape_articles_since(last_date))

            self.insert_articles(articles)

            self.logger.info(
                "Done scraping, sleeping for {} minutes".format(self.interval)
            )
            time.sleep(self.interval * 60)

    def test_list(self):
        """
        Display a list showing scraped articles
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
            "select distinct on (site_name) site_name, date from articles order by site_name, date desc"
        )
        results = self.db_cur.fetchall()
        return dict(map(lambda x: (x[0], datetime.fromisoformat(x[1])), results))
