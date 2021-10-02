import logging
import time
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver


class Scraper(ABC):
    def __init__(self, target: str, url: str, delay: int = 1):
        self.target = target
        self.url = url
        self.delay = delay
        self._driver = webdriver.Firefox()

    @abstractmethod
    def bypass_cookie(self, button_id: str, delay: int = None) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    def redirect(self, url: str, delay: int = None) -> None:
        logging.info('scraper redirected to: ' + url)
        self._driver.get(url)
        self._driver.implicitly_wait(delay or self.delay)

    def scroll(self, delay: int = None) -> None:
        self._driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(delay or self.delay)

    def get_content(self) -> BeautifulSoup:
        return BeautifulSoup(self._driver.page_source, 'lxml')

    def shutdown(self) -> None:
        logging.warning('scraper shutdown')
        self._driver.quit()
