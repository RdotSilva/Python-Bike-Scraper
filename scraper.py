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

        # Use a wait to make sure the page is ready to e scraped
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "crcPDP1")))
        except TimeoutException:
            print("URL took too long to load")
