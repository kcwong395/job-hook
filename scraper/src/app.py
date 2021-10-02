from datetime import datetime
import logging

from src.scraper.scraper_factory import ScraperFactory

if __name__ == '__main__':
    logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename='../log/' + datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S") + '.log',
                        level=logging.INFO)
    scraper = ScraperFactory.create("SG")
    if scraper:
        scraper.start()
