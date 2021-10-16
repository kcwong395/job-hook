from datetime import datetime
import logging
import yaml

from scraper.src.utils.db_utils import DbUtils
from scraper.src.scraper.scraper_factory import ScraperFactory

if __name__ == '__main__':
    logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename='../log/' + datetime.strftime(datetime.today(), "%Y-%m-%d %H-%M-%S") + '.log',
                        level=logging.INFO)

    with open("../../config.yaml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    DbUtils.connect(db_name=config['scraper']['db']['database'],
                    username=config['scraper']['db']['username'],
                    password=config['scraper']['db']['password'],
                    host=config['scraper']['db']['host'],
                    port=config['scraper']['db']['port'])
    targets = config['scraper']['targets']
    for target in targets:
        scraper = ScraperFactory.create(target)
        if scraper:
            scraper.start()
    DbUtils.close()

