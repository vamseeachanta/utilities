# Third party imports
import pandas as pd  # noqa
import scrapy
from scrapy import FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import (  # noqa useful while program is running
    open_in_browser,
)
import os #noqa
from io import BytesIO #noqa


class SpiderScrapy(scrapy.Spider):

    name = 'API_well_data'
    start_urls = ['https://www.data.bsee.gov/Well/APD/Default.aspx']

    def __init__(self, input_item=None, cfg=None, *args, **kwargs):
        super(SpiderScrapy, self).__init__(*args, **kwargs)
        self.input_item = input_item
        self.cfg = cfg

    def router(self, cfg):

        process = CrawlerProcess()

        for input_item in cfg['input']:
            process.crawl(SpiderScrapy, input_item=input_item, cfg=cfg)

        process.start()

    def parse(self, response):
        api_value = self.input_item['input_box']['value']
        api_value = str(api_value)
        data = {
            'ASPxFormLayout1$ASPxTextBoxAPI': api_value,
            'ASPxFormLayout1$ASPxButtonSubmitQ': 'Submit Query'
        }
        yield FormRequest.from_response(response,formdata=data, callback=self.step2)

    def step2(self, response):

        api_value = self.input_item['input_box']['value']
        api_value = str(api_value)
        data = {
            'ASPxFormLayout1$ASPxTextBoxAPI': api_value,
            '__EVENTTARGET': 'ASPxFormLayout2$btnCsvExport',
            '__EVENTARGUMENT': 'Click'
        }
        yield FormRequest.from_response(response,formdata=data, callback=self.parse_csv_data)

    def parse_csv_data(self, response): 
        label = self.input_item['label']
        API_number = self.input_item['input_box']['value']
        file_path = os.path.join(r'src\assetutilities\tests\test_data\web_scraping\results\Data', f'{label}.csv')

        with open(file_path, 'wb') as f:
            f.write(response.body)
            self.scraped_data = pd.read_csv(BytesIO(response.body))
            print()
            print(f"\n****The Scraped data of {API_number} ****\n")
            print(self.scraped_data)

