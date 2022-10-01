import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class SuperTaikyuScraping:
    def __init__(self):
        self.url: str = "https://www.supertaikyu.live/timings/"
        self.html = urlopen(self.url)
        self.soup = BeautifulSoup(self.html, "html.parser")

    def save_html(self) -> None:
        """
        This saves the html file to the current directory
        """
        with open("supertaikyu.html", "wb") as f:
            f.write(self.html.read())


def main():
    web_scraper = SuperTaikyuScraping()
    # print(web_scraper.soup.prettify())
    web_scraper.print_request()




if __name__ == "__main__":
    main()
    print("success")
