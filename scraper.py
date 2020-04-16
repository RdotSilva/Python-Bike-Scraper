from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client

from settings import to_number, from_number, twilio_sid, twilio_token


class Scraper(object):
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.delay = 3
        self.client = Client(twilio_sid, twilio_token)

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

        # Cookie Accept Button. Must be clicked every time we load the page
        cookie_button = self.driver.find_element_by_class_name("crc_cookie_accept")
        cookie_button.click()

        # Give list of selenium objects with class name of variant-option
        bike_stock = self.driver.find_elements_by_class_name("variant-option")

        # Locate bikes in stock
        # This will return a list of the SIZES of bike that are in stock
        # [M, L, XL]
        in_stock = self.driver.find_elements_by_xpath(
            "//div[@data-backorderable='true']"
        )

        print("Number of bikes in stock: ", len(in_stock))

        # Check bike stocks and email me if M in stock
        for bike in in_stock:
            print("Chain Reaction Stock Check: ")
            print(bike.text + " size is in stock!")

            if bike.text == "M":
                self.client.messages.create(
                    body=f"VRS Available https://www.chainreactioncycles.com/us/en/vitus-nucleus-29-vrs-bike-deore-1x10-2020/rp-prod181496",
                    from_=from_number,
                    to=to_number,
                )

    def quit(self):
        self.driver.close()
