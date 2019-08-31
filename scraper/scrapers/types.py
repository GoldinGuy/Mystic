from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    title: str
    url: str
    date: Optional[datetime]
    image_url: Optional[str]
    site_name: str
    site_url: str
    author_name: str
    author_url: Optional[str]

    def as_tuple(
        self
    ) -> (str, str, Optional[str], Optional[str], str, str, str, Optional[str]):
        return (
            self.title,
            self.url,
            None if self.date is None else self.date.isoformat(),
            self.image_url,
            self.site_name,
            self.site_url,
            self.author_name,
            self.author_url,
        )


class ScraperBase:
    def scrape_articles(self, page=1) -> List[Article]:
        pass

    def articles_since(self, date: datetime) -> List[Article]:
        articles = []

        page = 1

        articles.extend(self.scrape_articles(page))
        while articles[-1].date > date:
            page += 1
            articles.extend(self.scrape_articles(page))

        return articles
