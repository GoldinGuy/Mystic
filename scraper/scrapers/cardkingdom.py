from typing import List
import lxml.html
from datetime import datetime
import requests
import re

from .types import ScraperBase, Article

BASE_URL = "https://blog.cardkingdom.com/"
ARTICLES_TEMPLATE = "https://blog.cardkingdom.com/2019/page/{}/"


class CardKingdomScraper(ScraperBase):
    SITE_NAME = "Card Kingdom"

    def scrape_articles(self, page=1) -> List[Article]:
        # server rejects the default `requests` UA
        content = requests.get(
            ARTICLES_TEMPLATE.format(page),
            headers={"User-Agent": "Chrome/76.0.3809.110"},
        ).text

        content = lxml.html.fromstring(content)

        posts = content.xpath("//article")

        articles = []

        for post in posts:
            # print(lxml.html.tostring(post).decode())
            # break
            title_node = post.xpath("div/header/h2/a")[0]
            title = title_node.text
            url = title_node.attrib["href"]

            date_str = post.xpath("div/header/p/span[2]/time/text()")[0][1:]
            date = datetime.strptime(date_str, "%B %d, %Y")

            author_name = post.xpath("div/header/p/span/text()")[0][1:]

            img_url = post.xpath("div/a/img")[0].attrib["src"]

            article = Article(
                title,
                url,
                date,
                img_url,
                self.SITE_NAME,
                BASE_URL,
                author_name,
                author_url=None,
            )

            articles.append(article)

        return articles
