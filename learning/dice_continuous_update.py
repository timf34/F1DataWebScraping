from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time


# This is largely code copied from a tutorial on Real Python, except that I'll be using selenium instead of
# MechanicalSoup: https://realpython.com/python-web-scraping-practical-introduction/#interact-with-websites-in-real-time:~:text=For%20the%20die%20roll%20example%2C%20you%E2%80%99ll%20need%20to%20pass%20the%20number%2010%20to%20sleep().%20Here%E2%80%99s%20the%20updated%20program%3A


class SeleniumDiceRoll:
    def __init__(self):
        self.url: str = 'http://olympus.realpython.org/dice'
        # self.driver = webdriver.Edge()
        options = Options()
        options.headless = True
        self.driver = webdriver.Edge(options=options)


    def continuous_update_with_head(self):
        while True:
            self.driver.get(self.url)  # So this works... I'm not sure how robust it would be on the day though/ if its the best strategy/ way to do this...
            print(self.driver.find_element(By.TAG_NAME, "h2").text)
            time.sleep(1)


if __name__ == "__main__":
    scraper = SeleniumDiceRoll()
    scraper.continuous_update_with_head()
