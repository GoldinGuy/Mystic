from typing import List
from datetime import datetime
from threading import Thread
import lxml.html
import requests
import re

from .types import ScraperBase, Article

BASE_URL = "https://magic.wizards.com"
ARTICLES_TEMPLATE = (
    "https://magic.wizards.com/en/search-magic-ajax?fromDate={}&toDate={}"
    "&f1=article&f2=-1&sort=DESC&search=&l=en&offset={}"
)


class WizardsScraper(ScraperBase):
    SITE_NAME = "Wizards"
    background_img_regex = re.compile(r"url\((.*?)\)")

    def scrape_articles(self, page=1) -> List[Article]:
        today = datetime.today()
        last_year = datetime(today.year - 1, today.month, today.day)
        content = requests.get(
            ARTICLES_TEMPLATE.format(
                last_year.strftime("%m/%d/%Y"),
                today.strftime("%m/%d/%Y"),
                (page - 1) * 10,
            )
        ).json()
        articles = []
        threads = []

        for entry in content["data"]:
            content = lxml.html.fromstring(entry)

            link_node = content.xpath("//a")[0]
            url = BASE_URL + link_node.attrib["href"]

            category = content.xpath('//div[@class="text"]/h4/span')[0].text
            if category == "Wallpaper":
                continue

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
                title,
                url,
                date,
                img_url,
                self.SITE_NAME,
                BASE_URL,
                author_name,
                None,
                None,
            )

            articles.append(article)
            t = WizardsArticleFetcher(url)
            t.start()
            threads.append(t)

        for (article, thread) in zip(articles, threads):
            thread.join()
            if thread.result is None:
                continue
            article.description = thread.result

        return articles


class WizardsArticleFetcher(Thread):
    def __init__(self, url: str):
        self.url = url
        self.result = None
        super(WizardsArticleFetcher, self).__init__()

    @staticmethod
    def fetch_article_info(url: str) -> (str):
        content = lxml.html.fromstring(requests.get(url).text)

        return content.xpath('//meta[@name="description"]')[0].attrib["content"]

    def run(self):
        self.result = self.fetch_article_info(self.url)
