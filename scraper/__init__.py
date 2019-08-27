from typing import List

import psycopg2
import psycopg2.extensions
import logging

from .scrapers import ALL_SCRAPERS, ScraperBase


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
        self.logger.info("Scraping mtggoldfish")
        articles = []
        for scraper in self.scrapers:
            articles.extend(scraper.scrape_articles())

        print("Collected {} articles:".format(articles))
        for article in articles:
            print("#", article.title)
            print("  url    =", article.url)
            print("  image  =", article.image_url)
            print("  author = {} ({})".format(article.author_name, article.author_url))
            print("  site   = {} ({})".format(article.site_name, article.site_url))
            print()
