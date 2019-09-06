from typing import List
import lxml.html
import requests
from datetime import datetime
import re

from .types import ScraperBase, Article

BASE_URL = "https://article.hareruyamtg.com"
ARTICLES_TEMPLATE = "https://article.hareruyamtg.com/article/page/{}/?lang=en"
BACKGROUND_IMG_REGEX = re.compile(r"url\((.*?)\)")


class HareruyaScraper(ScraperBase):
    SITE_NAME = "Hareruya"

    def scrape_articles(self, page=1) -> List[Article]:
        content = requests.post(ARTICLES_TEMPLATE.format(page)).text

        content = lxml.html.fromstring(content)

        posts = content.xpath(
            '//article[@class="article-top__articleList__item col-md-4 col-xs-6"]/a'
        )
        articles = []
        for post in posts:
            url = BASE_URL + post.attrib["href"]

            img_node = post.xpath(
                'div/div[@class="article-top__articleList__item__thum"]'
            )[0]
            img_url = BACKGROUND_IMG_REGEX.search(img_node.attrib["style"]).group(1)

            info_node = post.xpath(
                'div/div[@class="article-top__articleList__item__info"]'
            )[0]

            author_name = info_node.xpath("div[2]/p")[0].text.strip()

            title = info_node.xpath("p[1]")[0].text.strip()
            date_str = info_node.xpath("p[2]")[0].text[:-6]
            date = datetime.strptime(date_str, "%Y/%m/%d")

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

        return articles
