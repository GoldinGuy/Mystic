from typing import List
from datetime import datetime
import lxml.html
import requests
import re

from .types import ScraperBase, Article

BASE_URL = "https://magic.wizards.com"
ARTICLES_TEMPLATE = "http://magic.tcgplayer.com/db/article_search_result.asp?page={}&ArticleDate={}&order_by="


class TCGPlayerScraper(ScraperBase):
    SITE_NAME = "TCGPlayer"
    background_img_regex = re.compile(r"url\((.*?)\)")

    def scrape_articles(self, page=1) -> List[Article]:
        today = datetime.today()
        last_3_months = datetime(today.year, today.month - 3, today.day)
        content = requests.get(
            ARTICLES_TEMPLATE.format(page, last_3_months.strftime("%m/%d/%Y")),
            headers={
                # "Trustworthy" headers (latest chrome)
                # attempts to convince incapsula we are an innocuous first time visitor
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.65 Safari/537.36",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "http://magic.tcgplayer.com/db/article_search_result.asp?page=1&ArticleDate=06/07/2019&order_by='",
                "Accept-Encoding": "gzip, deflate",
            },
        ).text

        content = lxml.html.fromstring(content)

        articles = []

        articles_wrap = content.xpath('//div[@class="articlesWrap"]')[0]

        author_nodes = articles_wrap.xpath("a[not(h2)]")
        # Hack (a[h2] doesn't seem to work)
        title_and_link_nodes = articles_wrap.xpath("a/h2/..")
        titles = articles_wrap.xpath("a/h2")
        descriptions = articles_wrap.xpath('div[@class="articleText"]')
        dates = articles_wrap.xpath("font/text()")

        for i in range(len(author_nodes)):
            title = titles[i].text
            url = BASE_URL + title_and_link_nodes[i].attrib["href"]
            date_str = dates[i][13:]
            date = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")

            author_name = author_nodes[i].text
            author_url = BASE_URL + author_nodes[i].attrib["href"]

            desc = descriptions[i].text

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
