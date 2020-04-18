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
        # self.driver = webdriver.Chrome()
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

    # Loads the url for Wiggle VRS
    def load_url_wiggle_vrs(self, url):
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-addToBasket"))
            )
            print("Wiggle VRS Page READY")
        except TimeoutException:
            print("Wiggle VRS Page took too long to load...")

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
    # Check CRC for VR stock
    def check_stock_crc_vr(self):


    def check_stock_wiggle_vrs(self):
        # Find the "select size" dropdown and scroll it into view
        stock_dropdown = self.driver.find_element_by_class_name("select-size-label")
        self.driver.execute_script("arguments[0].scrollIntoView();", stock_dropdown)

        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@data-colour='Military Green']")
                )
            ).click()
        except TimeoutException:
            print("Wait for dropdown to be clickable took too long")

        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//li[@for='101794155']"))
            )
            print("Wiggle VRS Medium dropdown is ready!")
            medium_bike = self.driver.find_element_by_xpath("//li[@for='101794155']")
        except TimeoutException:
            print("Wiggle VRS Page took too long to load...")

        # medium_bike = self.driver.find_element_by_xpath("//li[@for='101794155']")

        print("Checking Wiggle for stock... ")

        # Parse the text to make bike stock searchable
        medium_bike_split_text = medium_bike.text.split("$749.99")

        # Check the parsed text to see if bike is in stock
        # If bike in stock send text message
        if medium_bike_split_text[1].strip() == "Currently out of stock":
            print("Wiggle VRS out of stock")
        else:
            self.client.messages.create(
                body="VRS Available @ https://www.wiggle.com/vitus-nucleus-29-vrs-bike-deore-1x10-2020",
                from_=from_number,
                to=to_number,
            )

    def quit(self):
        self.driver.close()
