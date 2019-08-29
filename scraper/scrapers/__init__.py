from typing import Type, List

from .types import ScraperBase
from .mtggoldfish import MTGGoldfishScraper
from .edhrec import EDHRECScraper
from .channelfireball import ChannelFireballScraper
from .wizardsmagic import WizardsScraper
from .starcitygames import StarCityGamesScraper
from .hipsters import HipstersScraper


ALL_SCRAPERS: List[Type[ScraperBase]] = [
    MTGGoldfishScraper,
    ChannelFireballScraper,
    EDHRECScraper,
    WizardsScraper,
    StarCityGamesScraper,
    HipstersScraper,
]
