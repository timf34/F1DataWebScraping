import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class SuperTaikyuScraping:
    def __init__(self):
        self.url: str = "https://www.supertaikyu.live/timings/"
        self.driver = webdriver.Edge()
        self.html: str = self.get_html_using_selenium()
        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

    def get_html_using_selenium(self) -> str:
        self.driver.get(self.url)
        time.sleep(3)
        html = self.driver.page_source
        self.driver.close()
        return html

    def save_html(self) -> None:
        """
        This saves the html file to the current directory
        """
        print(self.html)
        with open("supertaikyu.html", "w", encoding="utf-8") as f:
            f.write(self.html)

    def print_soup(self) -> None:
        print(self.soup.prettify())


def main():
    web_scraper = SuperTaikyuScraping()
    web_scraper.save_html()


if __name__ == "__main__":
    main()
    print("success")
