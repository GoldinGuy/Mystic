from typing import List
import lxml.html
from datetime import datetime
import requests

from .types import ScraperBase, Article

SITE_NAME = "EDHREC"
BASE_URL = "https://articles.edhrec.com"
ARTICLES_TEMPLATE = "https://articles.edhrec.com/page/{}"


class EDHRECScraper(ScraperBase):
    def scrape_articles(self) -> List[Article]:
        content = lxml.html.fromstring(requests.get(ARTICLES_TEMPLATE.format(1)).text)

        posts = content.xpath('//div[@class="blog-post"]')

        articles = []

        for post in posts:
            # print(lxml.html.tostring(post).decode())

            title_node = post.xpath("h3/a")[0]
            title = title_node.text
            url = title_node.attrib["href"]

            meta_node = post.xpath('p[@class="blog-post-meta"]')[0]
            date = meta_node.text[:-9]
            # TODO: Fix null dates
            if date.strip() == "":
                date = datetime(1900, 1, 1, 0, 0)
            else:
                date = datetime.strptime(date, "%B %d, %Y")

            author_node = meta_node.xpath("a")[0]
            author_name = author_node.text.strip()
            author_url = author_node.attrib["href"]

            img_node = post.xpath('div[@class="preview"]/div/img')[0]
            img_url = img_node.attrib["src"]

            article = Article(
                title, url, date, img_url, SITE_NAME, BASE_URL, author_name, author_url
            )

            articles.append(article)

        return articles
