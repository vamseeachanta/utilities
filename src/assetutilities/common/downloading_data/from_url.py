import requests
import zipfile
import io
import pandas as pd
import os
from urllib.parse import urlparse

class DownloadingDataFromURL:
    
    def __init__(self):
        pass
    def router(self,cfg):
        
        urls = cfg['input_data']['urls']
        for url in urls.values():
            self.download_and_process_zip(url ,cfg)
        return cfg
    
    def download_and_process_zip(self, url ,cfg):

        # Extract the name from the URL 
        base_name_csv = os.path.basename(urlparse(url).path).replace('.zip', '')

        r = requests.get(url)
        r.raise_for_status()  # Check if the download was successful

        z = zipfile.ZipFile(io.BytesIO(r.content))
        extracted_files = z.namelist()

        txt_file = next((file for file in extracted_files if file.endswith('.txt')), None)
        if txt_file is None:
            raise FileNotFoundError("No .txt file found in the extracted ZIP file")

        with z.open(txt_file) as file:
            df = pd.read_csv(file, sep=',', encoding='ISO-8859-1', low_memory=False, nrows=100)
        
        output_dir = cfg['input_data']['out_directory']
        
        os.makedirs(output_dir, exist_ok=True)
        csv_filename = f"{base_name_csv}.csv"
        df.to_csv(os.path.join(output_dir, csv_filename), index=False)
    
        


