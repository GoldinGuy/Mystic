from typing import List
import json
from datetime import datetime
from threading import Thread
import lxml.html
from html import unescape
import requests

from .types import ScraperBase, Article

BASE_URL = "https://blog.cardsphere.com"
ARTICLES_TEMPLATE = "https://blog.cardsphere.com/page/{}/"


class CardSphereScraper(ScraperBase):
    SITE_NAME = "Cardsphere"

    def scrape_articles(self, page=1) -> List[Article]:
        content = requests.get(ARTICLES_TEMPLATE.format(page)).text
        threads = []

        content = lxml.html.fromstring(content)

        posts = content.xpath("//article")

        for post in posts:
            link_node = post.xpath("a")[0]
            url = BASE_URL + link_node.attrib["href"]

            t = CardSphereArticleFetcher(url)
            t.start()
            threads.append(t)

        articles = []

        for thread in threads:
            thread.join()
            if thread.result is None:
                continue
            articles.append(thread.result)

        return articles


class CardSphereArticleFetcher(Thread):
    def __init__(self, url: str):
        self.url = url
        self.result = None
        super(CardSphereArticleFetcher, self).__init__()

    @staticmethod
    def fetch_article_info(url: str) -> Article:
        content = lxml.html.fromstring(requests.get(url).text)
        meta = content.xpath('//script[@type="application/ld+json"]')[0].text
        meta = json.loads(meta)

        title = unescape(meta["headline"])
        date = datetime.strptime(
            meta["datePublished"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(microsecond=0, second=0)
        img_url = "https:" + meta["image"]["url"]
        author_name = meta["author"]["name"]
        author_url = meta["author"]["url"]
        description = unescape(meta["description"])

        return Article(
            title,
            url,
            date,
            img_url,
            CardSphereScraper.SITE_NAME,
            BASE_URL,
            author_name,
            author_url,
            description,
        )

    def run(self):
        self.result = self.fetch_article_info(self.url)
