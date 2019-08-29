from typing import List
from datetime import datetime
import lxml.html
import requests
import dateparser
import re

from .types import ScraperBase, Article

SITE_NAME = "Hipsters of the Coast"
BASE_URL = "https://www.hipstersofthecoast.com/"
ARTICLES_TEMPLATE = "https://www.hipstersofthecoast.com/?infinity=scrolling"
BACKGROUND_IMG_REGEX = re.compile(r"url\('(.*?)'\)")


class HipstersScraper(ScraperBase):
    def scrape_articles(self) -> List[Article]:
        today = datetime.today()
        content = requests.post(
            ARTICLES_TEMPLATE, data={"page": "0", "order": "DESC"}
        ).json()

        articles = []

        content = lxml.html.fromstring(content["html"])

        posts = content.xpath('//div[@class="post_container"]')
        for post in posts:

            body_node = post.xpath("div")[0]

            title_node = body_node.xpath('div[@class="post-title"]/h3/a')[0]
            title = title_node.text.strip()
            url = title_node.attrib["href"]

            category = body_node.xpath('div[@class="post-category"]/h4/a')[
                0
            ].text.strip()
            if category == "ADVERTISEMENT":
                continue

            date, img_url, author_name, author_url = self.fetch_article_info(url)

            article = Article(
                title, url, date, img_url, SITE_NAME, BASE_URL, author_name, author_url
            )

            articles.append(article)

        return articles

    def fetch_article_info(self, url: str) -> (str, str, str, str):
        content = lxml.html.fromstring(requests.get(url).text)

        date = content.xpath('//div[@class="post-date"]/p')[0].text.strip()
        date = dateparser.parse(date)

        author_node = content.xpath(
            '//div[@class="post-author-container"]/div/div/p/a'
        )[0]
        author_name = author_node.text
        author_url = author_node.attrib["href"]

        img_node = content.xpath('//div[@class="postimg_single"]')[0]

        img_url = BACKGROUND_IMG_REGEX.search(img_node.attrib["style"]).group(1)

        return (date, img_url, author_name, author_url)
