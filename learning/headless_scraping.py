from selenium import webdriver


class HeadlessEdgeScraper():
    def __init__(self):
        self.url = "https://www.google.com"
        self.options = webdriver.EdgeOptions()
        self.options.headless = True
        self.driver = webdriver.Edge(options=self.options)

    def get_page(self):
        self.driver.get(self.url)
        print(self.driver.title)
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    scraper = HeadlessEdgeScraper()
    scraper.get_page()
