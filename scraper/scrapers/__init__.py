from typing import Type, List

from .types import ScraperBase
from .mtggoldfish import MTGGoldfishScraper


ALL_SCRAPERS: List[Type[ScraperBase]] = [MTGGoldfishScraper]
