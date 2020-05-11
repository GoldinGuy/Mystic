from typing import List
import lxml.html
from datetime import datetime
import requests

from .types import ScraperBase, Article

BASE_URL = "https://www.coolstuffinc.com/"
ARTICLES_TEMPLATE = "https://www.coolstuffinc.com/a/?action=&page={}"


class CoolStuffScraper(ScraperBase):
    SITE_NAME = "CoolStuffInc"

    def scrape_articles(self, page=1) -> List[Article]:
        # server rejects the default `requests` UA
        content = requests.get(
            ARTICLES_TEMPLATE.format(page),
            headers={"User-Agent": "Chrome/76.0.3809.110"},
        ).text
        content = lxml.html.fromstring(content)

        posts = content.xpath('//ul[@class="gm-article-preview-list column"]/li')

        articles = []

        for post in posts:
            title_node = post.xpath("div/h1/a")[0]
            title = title_node.text
            url = BASE_URL + title_node.attrib["href"]

            author_node, _, date_node = post.xpath("div/div/span")
            author_name = author_node.text
            date = datetime.strptime(date_node.text, "%B %d, %Y")

            desc = post.xpath("div/div[2]")[0].text

            article = Article(
                title,
                url,
                date,
                None,
                self.SITE_NAME,
                BASE_URL,
                author_name,
                None,
                desc,
            )

            articles.append(article)

        return articles
