from selenium import webdriver


class Scraper(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.delay = 3
