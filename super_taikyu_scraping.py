import bs4
import boto3
import time
import sys

from bs4 import BeautifulSoup
from dataclasses import asdict
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from typing import List, Union

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY
from config import TimingTableCar, TimingTable
from utils import open_object_using_pickle


class SuperTaikyuScraping:
    def __init__(self, use_local_html: bool = False, headless: bool = True):
        self.url: str = "https://www.supertaikyu.live/timings/"
        if use_local_html:
            self.html: str = open("supertaikyu.html", "r", encoding="utf-8").read()
        elif not headless:
            self.driver = webdriver.Edge()
            self.html: str = self.get_html_using_selenium()
        else:
            self.html = ""
            pass
            # raise NotImplementedError("Headless scraping is implemented in a child class")
        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

        self.tables: List[str] = self.soup.find_all("table")
        self.headless: bool = headless
        self.timing_table: bs4.ResultSet = self.soup.find_all("table", {"class": "table01", "id": "timing_table"})  # This will work for any of the id's in the tables

    def get_html_using_selenium(self, delay: int = 3) -> str:
        self.driver.get(self.url)
        time.sleep(delay)
        html = self.driver.page_source
        # Note: we are using headless mode solely for continuous updates here... although we could probs use it in general.
        if not self.headless:
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

    def working_with_timing_table(self, print_tables: bool = False ) -> TimingTable:

        # Initialize our table data store
        table_db: TimingTable = TimingTable()

        # Find all rows in self.timing_table[0] that contain the 'data-name' attribute
        rows = self.timing_table[0].find_all("tr", {"data-name": True})
        for row in rows:
            car_db = TimingTableCar()  # Initialize a new TimingTableCar
            cols = row.find_all("td")   # Find all columns in the row (all data cells within the row)
            for index, col in enumerate(cols):
                car_db[index] = col.text  # Add the text of the column to the TimingTableCar via the index
            table_db.cars[car_db.car_num] = car_db  # Add the car to the table, where the key is the car_number

        if print_tables:
            print(f"table_db.cars: \n {table_db.cars}")
            print(f"len(table_db.cars): {len(table_db.cars)}")
        return table_db


class SuperTaikyuScrapingHeadless(SuperTaikyuScraping):
    def __init__(self):
        super().__init__(headless=True)
        options = Options()
        options.headless = True
        self.driver = webdriver.Edge(options=options)

    def continuous_update(self):
        while True:
            self.html = self.get_html_using_selenium(delay=1)
            self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")
            self.timing_table: bs4.ResultSet = self.soup.find_all("table", {"class": "table01", "id": "timing_table"})
            self.working_with_timing_table()
            print("The time is: ", time.ctime())


class ConvertTimingTableToList:
    """
        This class is for converting the TimingTable object to a List object suitable for sending to our device
        via MQTT.
        This works for live timing data as well (i.e. straight from our web scraper) as from a pickle file.
    """
    def __init__(self, live_timing_table: TimingTable, live_data: bool = False):
        if live_data:
            if live_timing_table is None:
                raise ValueError("live_timing_table is None")
            else:
                self.timing_table = live_timing_table
        else:
            self.timing_table: TimingTable = open_object_using_pickle("timing_table_object.pkl")
            # self.timing_table_list: List[List[str]] = self.convert_timing_table_to_list()

    def convert_timing_table_to_list(self, list_of_lists: bool = False) -> Union[List[str], List[List[str]]]:
        # Reinitialize self.timing_table_cars as the same dict but with the keys sorted alphabetically
        self.timing_table.cars = dict(sorted(self.timing_table.cars.items(), key=lambda item: item[0]))

        if list_of_lists:
            return [list(asdict(car).values()) for car in self.timing_table.cars.values()]
        else:
            # big_list = []
            # for car in self.timing_table.cars.values():
            #     big_list.extend(list(asdict(car).values()))
            #     big_list.extend("\n")
            # return big_list

            # Make a faster version of the above loop, including the newline (copilot is amazing)
            return [item for sublist in [[*asdict(car).values(), "\n"] for car in self.timing_table.cars.values()] for item in sublist]


class SendTimingTableToMQTT:
    def __init__(self, topic: str = "RACE/3"):
        self.access_key: str = ACCESS_KEY
        self.secret_key: str = SECRET_ACCESS_KEY
        self.topic: str = topic
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')

    def publish_to_topic(self, data) -> None:
        response = self.iot_client.publish(
            topic=self.topic,
            qos=1,
            payload=str(data)
        )




def main():
    # web_scraper = SuperTaikyuScraping(use_local_html=True)
    # web_scraper.save_soup()
    # # web_scraper.working_with_rows()
    # # web_scraper.working_with_headers()
    # web_scraper.working_with_timing_table()

    # continous_scraper = SuperTaikyuScrapingHeadless()
    # continous_scraper.continuous_update()

    converter = ConvertTimingTableToList()
    sample_list = converter.convert_timing_table_to_list()

    # Print the memory usage of the list
    print("Memory usage of list: ", sys.getsizeof(sample_list))

    # Initialize our MQTT client
    mqtt_client = SendTimingTableToMQTT()
    mqtt_client.publish_to_topic(sample_list)


if __name__ == "__main__":
    main()
    print("Done.")
