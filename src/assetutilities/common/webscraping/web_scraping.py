# Third party imports
# Reader imports
from assetutilities.common.webscraping.scrapper_scrapy import SipderScrapy
from assetutilities.common.webscraping.scrapper_bs4 import BS4Scrapper
from scrapy.crawler import CrawlerProcess


# A class for scraping web pages. 
# Class gives option to choose of the following methods:
# 1. BeautifulSoup and requests
# 2. Selenium
# 3. Scrapy

ss = SipderScrapy()
bs4s = BS4Scrapper()

class WebScraping:
    def __init__(self):
        pass

    def router(self, cfg):

        web_scrape_engine = cfg['web_scrape_engine']

        if web_scrape_engine == 'beautiful_soup':
            return self.beautiful_soup()
        elif web_scrape_engine == 'selenium':
            return self.selenium()
        elif web_scrape_engine == 'scrapy':
            return self.scrapy()

        # Check data exists

    def beautiful_soup(self):
        bs4s.router()

    def selenium(self):
        pass

    def scrapy(self):
        process = CrawlerProcess()
        process.crawl(SipderScrapy)
        process.start()



