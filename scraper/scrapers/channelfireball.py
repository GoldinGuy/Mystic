from typing import List
from datetime import datetime
import requests
import lxml.html

from .types import ScraperBase, Article

BASE_URL = "https://www.channelfireball.com/all-strategy"
ARTICLES_TEMPLATE = (
    "https://www.channelfireball.com/all-strategy/category/articles/page/{}"
)


class ChannelFireballScraper(ScraperBase):
    SITE_NAME = "ChannelFireball"

    def scrape_articles(self, page=1) -> List[Article]:
        # server rejects the default `requests` UA
        content = requests.get(
            ARTICLES_TEMPLATE.format(page),
            headers={"User-Agent": "Chrome/76.0.3809.110"},
        ).text
        content = lxml.html.fromstring(content)

        posts = content.xpath("//article/div/div")

        articles = []

        for post in posts:
            header_node = post.xpath("header")[0]
            title_node = header_node.xpath("h2/a")[0]
            title = title_node.text
            url = title_node.attrib["href"]

            author_url = header_node.xpath("div/span/a")[0].attrib["href"]
            author_name = header_node.xpath("div/span/a/span")[0].text

            date_str = header_node.xpath("div/span[2]/span")[0].text.strip()
            date = datetime.strptime(date_str, "%B %d, %Y")

            img_url = post.xpath("div/div/a/img")[0].attrib["src"]

            desc = post.xpath("div[2]/p")[0].text

            article = Article(
                title,
                url,
                date,
                img_url,
                self.SITE_NAME,
                BASE_URL,
                author_name,
                author_url,
                desc,
            )

            articles.append(article)

        return articles
