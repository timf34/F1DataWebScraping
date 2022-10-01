from selenium import webdriver
from bs4 import BeautifulSoup
import time

import requests

class WebScraper:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.url: str = "https://www.supertaikyu.live/timings/"

    def get_html_using_selenium(self) -> None:
        self.driver.get(self.url)
        time.sleep(5)
        # Check this out for a better solution later on: https://stackoverflow.com/questions/25221580/waiting-for-a-table-to-load-completely-using-selenium-with-python
        self.html = self.driver.page_source
        print("html: ", self.html)
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.driver.close()

    def get_html_using_requests(self) -> None:
        """
        Getting html using requests.get with user-agent headers
        """
        self.html = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        self.soup = BeautifulSoup(self.html.text, "html.parser")

    def print_html(self) -> None:
        print("printing soup: ")
        print(self.soup.prettify())


def main():
    web_scraper = WebScraper()
    web_scraper.get_html_using_selenium()
    # web_scraper.print_html()


if __name__ == '__main__':
    main()