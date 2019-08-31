from typing import List
from datetime import datetime
import requests
import html

from .types import ScraperBase, Article

BASE_URL = "https://store.channelfireball.com/landing"
ARTICLES_TEMPLATE = (
    "https://chfireball.wpengine.com/wp-json/wp/v2/multiple-post-type?"
    "&type[]=post&per_page=15&page={}"
)


class ChannelFireballScraper(ScraperBase):
    SITE_NAME = "ChannelFireball"

    def scrape_articles(self, page=1) -> List[Article]:
        # server rejects the default `requests` UA
        content = requests.get(
            ARTICLES_TEMPLATE.format(page),
            headers={"User-Agent": "Chrome/76.0.3809.110"},
        ).json()

        articles = []

        for entry in content:
            article = Article(
                html.unescape(entry["title"]),
                entry["link"],
                datetime.fromisoformat(entry["date"]),
                entry["featured_image"]["thumb"],
                self.SITE_NAME,
                BASE_URL,
                entry["author"],
                None,
            )

            articles.append(article)

        return articles
