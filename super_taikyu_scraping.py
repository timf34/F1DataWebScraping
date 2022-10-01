import bs4
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from typing import List
import time

from config import TimingTable


class SuperTaikyuScraping:
    def __init__(self, use_local_html: bool = False):
        self.url: str = "https://www.supertaikyu.live/timings/"
        if use_local_html:
            self.html: str = open("supertaikyu.html", "r", encoding="utf-8").read()
        else:
            self.driver = webdriver.Edge()
            self.html: str = self.get_html_using_selenium()
        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

        self.tables: List[str] = self.soup.find_all("table")
        self.timing_table: bs4.ResultSet = self.soup.find_all("table", {"class": "table01", "id": "timing_table"})  # This will work for any of the id's in the tables

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

    def save_soup(self) -> None:
        with open("supertaikyu_soup.txt", "w", encoding="utf-8") as f:
            f.write(self.soup.prettify())

    def print_soup(self) -> None:
        # print("html: \n", self.html)
        print("soup: \n", self.soup.prettify())

    def working_with_rows(self) -> None:
        for table in self.tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                for col in cols:
                    print(col.text)  # Note that this will print blank lines when there is no text
                print("new row")

    def working_with_headers(self) -> None:
        for table in self.tables:
            headers = table.find_all("th")
            for header in headers:
                print(header.text)
            print("\nnew table")

    def working_with_timing_table(self) -> None:
        # Find all rows in self.timing_table[0] that contain the 'data-name' attribute
        rows = self.timing_table[0].find_all("tr", {"data-name": True})
        for row in rows[0:1]:
            cols = row.find_all("td")   # Find all columns in the row
            for index, col in enumerate(cols):
                print(index, col.text)
                if col.text == "":
                    print("None")
                print("new col")



def main():
    web_scraper = SuperTaikyuScraping(use_local_html=True)
    web_scraper.save_soup()
    # web_scraper.working_with_rows()
    # web_scraper.working_with_headers()

    web_scraper.working_with_timing_table()


if __name__ == "__main__":
    main()
    print("success")
