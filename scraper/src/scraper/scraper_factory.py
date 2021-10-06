import logging

from src.scraper.scraper import Scraper
from src.scraper.scraper_sg import ScraperSG


class ScraperFactory:

    site_scrapers = {
        "SG": ScraperSG,
    }

    """
    input the site to scrap and return the corresponding site scraper
    """
    @staticmethod
    def create(site: str) -> Scraper:
        if site in ScraperFactory.site_scrapers:
            return ScraperFactory.site_scrapers[site](target="Société Générale")
        logging.error('Unrecognized Site: ' + site)
