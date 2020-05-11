from typing import List
import lxml.html
from datetime import datetime
import requests

from .types import ScraperBase, Article

BASE_URL = "http://www.starcitygames.com"


class StarCityGamesScraper(ScraperBase):
    SITE_NAME = "StarCityGames"

    def scrape_articles_since(self, date: datetime) -> List[Article]:
        return self.scrape_articles()

    # TODO: Make actually do paging
    def scrape_articles(self, page=1) -> List[Article]:
        content = lxml.html.fromstring(
            requests.get("http://www.starcitygames.com/tags/Select/").text
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

            if (
                header_node.xpath('p[@class="search_tag"]/img')[0]
                .attrib["src"]
                .endswith("premium.jpg")
            ):
                continue

            date_raw = header_node.xpath('p[@class="tag_article_date"]')[0].text

            desc = post.xpath("p")[0].text_content()

            date = self.parse_date(date_raw)
            img_url = None

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

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        today = datetime.today()
        if date_str == "TODAY":
            return today.replace(microsecond=0, second=0)
        else:
            return datetime.strptime(date_str, "%m/%d").replace(year=today.year)
