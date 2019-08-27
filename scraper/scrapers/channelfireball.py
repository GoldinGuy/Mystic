from typing import List
from datetime import datetime
import requests

from .types import ScraperBase, Article

SITE_NAME = "ChannelFireball"
BASE_URL = "https://store.channelfireball.com/landing"
ARTICLES_TEMPLATE = (
    "https://chfireball.wpengine.com/wp-json/wp/v2/multiple-post-type?"
    "&type[]=post&type[]=video&per_page=15"
)


class ChannelFireballScraper(ScraperBase):
    def scrape_articles(self) -> List[Article]:
        # server rejects the default `requests` UA
        content = requests.get(
            ARTICLES_TEMPLATE.format(1), headers={"User-Agent": "Chrome/76.0.3809.110"}
        ).json()

        articles = []

        for entry in content:

            article = Article(
                entry["title"],
                entry["link"],
                datetime.fromisoformat(entry["date"]),
                entry["featured_image"]["thumb"],
                SITE_NAME,
                BASE_URL,
                entry["author"],
                None,
            )

            articles.append(article)

        return articles
