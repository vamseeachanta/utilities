# Standard library imports
import os #noqa
from io import BytesIO #noqa

import pandas as pd
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

class BS4Scrapper:
    
    def __init__(self):
        pass

    def router(self, cfg):

        self.input_data(cfg)
        return cfg
    
    def input_data(self, cfg):
        master_settings = cfg['input_settings']
        for input_item in cfg['input']:
            input_item = {**master_settings, **input_item}
            self.get_data(cfg, input_item)

    def get_data(self, cfg, input_item):

        url = input_item['url']
        API_number = input_item['input_box']['value']

        session = requests.Session()  

        response = session.get(url) # GET request to the form page
        soup = BeautifulSoup(response.content, 'html.parser') 

        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

        api_submit_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': eventvalidation,
            'ASPxFormLayout1$ASPxTextBoxAPI': API_number, 
            'ASPxFormLayout1$ASPxButtonSubmitQ': 'Submit Query'  # The submit button
        }

        # Submit the API form 
        response = session.post(url, data=api_submit_payload)
        soup = BeautifulSoup(response.content, 'html.parser')

        if response.status_code == 200:
            print(f"API {API_number}{Fore.GREEN} submission successful!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to submit API {API_number}{Style.RESET_ALL}. Status code: {response.status_code}")

        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']

        csv_export_payload = {
            '__EVENTTARGET': 'ASPxFormLayout2$btnCsvExport',  # Targeting the CSV button
            '__EVENTARGUMENT': 'Click',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': eventvalidation
        }

        csv_response = session.post(url, data=csv_export_payload)

        label = input_item['label']
        output_path = input_item['output_dir']
        csv_path = os.path.join(output_path, f"{label}.csv")

        if csv_response.status_code == 200:
            with open(csv_path, 'wb') as f:
                f.write(csv_response.content)
                df = pd.read_csv(BytesIO(csv_response.content)) # class <bytes> to pandas df
                print()
                print(f"****The Scraped data of {API_number} ****\n\n")
                print(df)
        else:
            print(f"{Fore.RED}Failed to export CSV.{Style.RESET_ALL} Status code: {csv_response.status_code}")

    