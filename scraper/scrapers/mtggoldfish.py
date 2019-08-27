from typing import List
import re
import lxml.html
import requests

from .types import ScraperBase, Article

SITE_NAME = "MTGGoldfish"
BASE_URL = "https://www.mtggoldfish.com"
ARTICLES_TEMPLATE = "https://www.mtggoldfish.com/articles?page={}"


class MTGGoldfishScraper(ScraperBase):
    background_img_regex = re.compile(r"url\('(.*?)'\)")

    def scrape_articles(self) -> List[Article]:
        content = lxml.html.fromstring(requests.get(ARTICLES_TEMPLATE.format(1)).text)

        cards = content.xpath('//div[@class="article-tile"]')

        articles = []

        for card in cards:
            card_bg = card.xpath("div/div/div")[0]
            img_url = self.background_img_regex.search(card_bg.attrib["style"]).group(1)

            title_node = card.xpath('h2[@class="article-tile-title"]/a')[0]
            title = title_node.text
            url = BASE_URL + title_node.attrib["href"]

            author_node = card.xpath("h3/a")[0]
            author_name = author_node.text
            author_url = BASE_URL + author_node.attrib["href"]

            article = Article(
                title, url, img_url, SITE_NAME, BASE_URL, author_name, author_url
            )

            articles.append(article)

        return articles
