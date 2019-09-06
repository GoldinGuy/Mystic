from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

ArticleTupleType = (
    str,
    str,
    Optional[str],
    Optional[str],
    str,
    str,
    Optional[str],
    Optional[str],
    Optional[str],
)


@dataclass
class Article:
    title: str
    url: str
    date: Optional[datetime]
    image_url: Optional[str]
    site_name: str
    site_url: str
    author_name: Optional[str]
    author_url: Optional[str]
    description: Optional[str]

    def as_tuple(self) -> ArticleTupleType:
        return (
            self.title,
            self.url,
            None if self.date is None else self.date.isoformat(),
            self.image_url,
            self.site_name,
            self.site_url,
            self.author_name,
            self.author_url,
            self.description,
        )


class ScraperBase:
    SITE_NAME: str

    def scrape_articles(self, page=1) -> List[Article]:
        pass

    def scrape_articles_since(self, date: datetime) -> List[Article]:
        articles = []

        page = 1

        articles.extend(self.scrape_articles(page))
        while articles[-1].date > date:
            page += 1
            articles.extend(self.scrape_articles(page))

        return articles
