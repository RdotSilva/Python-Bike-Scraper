from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Scraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.delay = 3

    # Loads the specified url.
    def load_crc_vrs_url(self, url):
        self.driver.get(url)

        # Use a wait to make sure the page is ready to be scraped
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "crcPDP1")))
        except TimeoutException:
            print("URL took too long to load")

    # Check the page to see if the bike is in stock
    def check_stock_crc_vrs(self):
        # Wait for Accept Cookie Button to be present. Without clicking this button you can't scrape the page.
        # This button will pop up every time we reload the page.
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "crc_accept_cookie"))
            )
        except TimeoutException:
            print("Accept Cookie Button took too long to load")
