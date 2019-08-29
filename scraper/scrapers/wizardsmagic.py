from typing import List
from datetime import datetime
import lxml.html
import requests
import re

from .types import ScraperBase, Article

SITE_NAME = "Wizards"
BASE_URL = "https://magic.wizards.com"
ARTICLES_TEMPLATE = (
    "https://magic.wizards.com/en/search-magic-ajax?fromDate={}&toDate={}"
    "&f1=article&f2=-1&sort=DESC&search=&l=en&offset={}"
)


class WizardsScraper(ScraperBase):
    background_img_regex = re.compile(r"url\((.*?)\)")

    def scrape_articles(self) -> List[Article]:
        today = datetime.today()
        last_year = datetime(today.year - 1, today.month, today.day)
        content = requests.get(
            ARTICLES_TEMPLATE.format(
                last_year.strftime("%m/%d/%Y"), today.strftime("%m/%d/%Y"), 1
            )
        ).json()
        articles = []

        for entry in content["data"]:
            content = lxml.html.fromstring(entry)

            link_node = content.xpath("//a")[0]
            url = BASE_URL + link_node.attrib["href"]

            body_node = content.xpath('//div[@class="text"]/div[@class="title"]')[0]
            title = body_node.xpath("h3")[0].text
            author_name = body_node.xpath('p/span[@class="author"]')[0].text[3:]

            date_node = body_node.xpath('p/span[@class="date"]')[0]
            date = "".join(map(lambda x: x.text, date_node.getchildren()))

            date = datetime.strptime(date, " %B %d %Y ")

            img_node = content.xpath('//div[@class="image"]')[0]
            img_url = self.background_img_regex.search(img_node.attrib["style"]).group(
                1
            )

            article = Article(
                title, url, date, img_url, SITE_NAME, BASE_URL, author_name, None
            )

            articles.append(article)

        return articles
