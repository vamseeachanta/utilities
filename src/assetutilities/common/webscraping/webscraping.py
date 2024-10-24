# A class for scraping web pages. 
# Class gives option to choose of the following methods:
# 1. BeautifulSoup and Requests
# 2. Selenium
# 3. Scrapy


class WebScraping:
    def __init__(self, url):
        self.url = url

    def router(self, method):

        if method == 'beautiful_soup':
            return self.beautiful_soup()
        elif method == 'selenium':
            return self.selenium()
        elif method == 'scrapy':
            return self.scrapy()

        # Check data exists

    def beautiful_soup(self):
        pass

    def selenium(self):
        pass

    def scrapy(self):
        pass

