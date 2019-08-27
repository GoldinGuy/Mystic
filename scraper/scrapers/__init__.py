from typing import Type, List

from .types import ScraperBase
from .mtggoldfish import MTGGoldfishScraper
from .channelfireball import ChannelFireballScraper


ALL_SCRAPERS: List[Type[ScraperBase]] = [MTGGoldfishScraper, ChannelFireballScraper]
