import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class SuperTaikyuScraping:
    def __init__(self, use_local_html: bool = False):
        self.url: str = "https://www.supertaikyu.live/timings/"
        if use_local_html:
            self.html: str = open("supertaikyu.html", "r", encoding="utf-8").read()
        else:
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
        with open("supertaikyu.html", "w", encoding="utf-8") as f:
            f.write(self.html)

    def print_soup(self) -> None:
        # print("html: \n", self.html)
        print("soup: \n", self.soup.prettify())


def main():
    web_scraper = SuperTaikyuScraping(use_local_html=True)
    web_scraper.print_soup()


if __name__ == "__main__":
    main()
    print("success")
