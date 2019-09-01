from typing import List
from datetime import datetime
import lxml.html
import requests

from .types import ScraperBase, Article

BASE_URL = "https://magic.wizards.com"
ARTICLES_TEMPLATE = (
    "https://magic.wizards.com/en/see-more-podcast?page={}&filter_by=DESC"
)


class WizardsPodcastsScraper(ScraperBase):
    SITE_NAME = "Wizards Podcasts"

    def scrape_articles(self, page=1) -> List[Article]:
        content = requests.get(ARTICLES_TEMPLATE.format(page)).json()
        articles = []

        content = lxml.html.fromstring(content["data"])

        entries = content.xpath('//div[@class="ark-podcast-list-item"]')

        for entry in entries:
            title = entry.xpath("div/div/h5")[0].text
            url = entry.xpath("div[2]/div/div[2]/a")[0].attrib["href"]
            date_node = entry.xpath("div[1]")[0]
            date_str = "".join(map(lambda x: x.text, date_node.getchildren()))
            date = datetime.strptime(date_str, " %b %d %Y ")

            article = Article(
                title, url, date, None, self.SITE_NAME, BASE_URL, None, None
            )

            articles.append(article)

        return articles
