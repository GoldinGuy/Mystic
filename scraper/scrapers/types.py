from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    title: str
    url: str
    date: datetime
    image_url: Optional[str]
    site_name: str
    site_url: str
    author_name: str
    author_url: Optional[str]


class ScraperBase:
    def scrape_articles(self) -> List[Article]:
        pass
