from scraper import Scraper

crc_vrs_url = "https://www.chainreactioncycles.com/us/en/vitus-nucleus-29-vrs-bike-deore-1x10-2020/rp-prod181496"

# Create new instance of scraper
crc_vrs_scraper = Scraper()

# Load crc vrs url and  check for stock
crc_vrs_scraper.load_crc_vrs_url(crc_vrs_url)
crc_vrs_scraper.check_stock_crc_vrs()
