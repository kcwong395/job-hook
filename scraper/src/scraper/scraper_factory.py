import logging

from scraper.src.scraper.scraper import Scraper
from scraper.src.scraper.scraper_sg import ScraperSG


class ScraperFactory:

    _site_scrapers = {
        "SG": ScraperSG,
    }

    """
    input the site to scrap and return the corresponding site scraper
    """
    @staticmethod
    def create(site: str) -> Scraper:
        if site in ScraperFactory._site_scrapers:
            return ScraperFactory._site_scrapers[site](target="Société Générale")
        logging.error('Unrecognized Site: ' + site)
