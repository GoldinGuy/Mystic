from typing import List
import lxml.html
from datetime import datetime
import requests

from .types import ScraperBase, Article

SITE_NAME = "StarCityGames"
BASE_URL = "http://www.starcitygames.com"


class StarCityGamesScraper(ScraperBase):
    def scrape_articles(self) -> List[Article]:
        content = lxml.html.fromstring(
            requests.get("http://www.starcitygames.com/tags/Premium~Select/").text
        )

        posts = content.xpath('//article[@class="articles all"]')

        articles = []

        for post in posts:
            header_node = post.xpath("header")[0]

            title_node = header_node.xpath('p[@class="premium_title"]/a')[0]
            title = title_node.text
            url = title_node.attrib["href"]

            author_name = header_node.xpath('p[@class="premium_author"]')[
                0
            ].text.strip()
            author_url = post.xpath('footer/div[@class="right"]/a')[0].attrib["href"]

            date_raw = header_node.xpath('p[@class="tag_article_date"]')[0].text

            date = self.parse_date(date_raw)
            img_url = None
            article = Article(
                title, url, date, img_url, SITE_NAME, BASE_URL, author_name, author_url
            )
            print(article)
            articles.append(article)

        return articles

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        if date_str == "TODAY":
            return datetime.today()
        else:
            today = datetime.today()
            parsed = datetime.strptime(date_str, "%m/%d")
            return datetime(today.year, parsed.month, parsed.day)
