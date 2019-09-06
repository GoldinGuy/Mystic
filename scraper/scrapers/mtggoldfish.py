from typing import List
import re
import lxml.html
import requests
from datetime import datetime

from .types import ScraperBase, Article

BASE_URL = "https://www.mtggoldfish.com"
ARTICLES_TEMPLATE = "https://www.mtggoldfish.com/articles?page={}"


class MTGGoldfishScraper(ScraperBase):
    SITE_NAME = "MTGGoldfish"
    background_img_regex = re.compile(r"url\('(.*?)'\)")

    def scrape_articles(self, page=1) -> List[Article]:
        content = lxml.html.fromstring(
            requests.get(ARTICLES_TEMPLATE.format(page)).text
        )

        cards = content.xpath('//div[@class="article-tile"]')

        articles = []

        for card in cards:
            card_bg = card.xpath("div/div/div")[0]
            img_url = self.background_img_regex.search(card_bg.attrib["style"]).group(1)

            title_node = card.xpath('h2[@class="article-tile-title"]/a')[0]
            title = title_node.text
            url = BASE_URL + title_node.attrib["href"]

            # TODO: Ensure year is correct by fetching article page which has year
            date_node = card.xpath("h3")[0]
            date_str = date_node.text[1:-7]
            date = parse_short_date(date_str)

            author_node = date_node.xpath("a")[0]
            author_name = author_node.text
            author_url = BASE_URL + author_node.attrib["href"]

            desc = card.xpath("p")[0].text

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


def parse_short_date(date: str) -> datetime:
    today = datetime.today()
    return datetime.strptime(date, "%b %d").replace(year=today.year)
