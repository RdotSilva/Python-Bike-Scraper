from scraper import Scraper

crc_vrs_url = "https://www.chainreactioncycles.com/us/en/vitus-nucleus-29-vrs-bike-deore-1x10-2020/rp-prod181496"
crc_vr_url = "https://www.chainreactioncycles.com/us/en/vitus-nucleus-29-vr-bike-altus-2x9-2020/rp-prod181494"
wiggle_vrs_url = "https://www.wiggle.com/vitus-nucleus-29-vrs-bike-deore-1x10-2020"


# Create new instance of scraper
crc_vrs_scraper = Scraper()
wiggle_vrs_scraper = Scraper()

# Load crc vrs url and  check for stock
crc_vrs_scraper.load_crc_vrs_url(crc_vrs_url)
crc_vrs_scraper.check_stock_crc_vrs()
crc_vrs_scraper.quit()

# Load Wiggle VRS url and check for stock
wiggle_vrs_scraper.load_url_wiggle_vrs(wiggle_vrs_url)
wiggle_vrs_scraper.check_stock_wiggle_vrs()
wiggle_vrs_scraper.quit()
