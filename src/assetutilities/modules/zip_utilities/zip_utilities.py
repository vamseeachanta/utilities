# Standard library imports
import os


from zipfile import ZipFile

class ZipUtilities:
    def __init__(self):
        pass

    def router(self, cfg):
        if cfg['analysis_settings']['flag']:
            if cfg['analysis_settings']['by'] == 'stem':
                self.zip_files_by_stem(cfg)
        else:
            raise NotImplementedError

    def zip_files_by_stem(self, cfg):
        '''
        Zips files in analysis_settings directory 
        Uses stem name from file_management settings
        '''
        file_extensions = cfg['file_management']['files']['files_in_current_directory']['file_extensions']
        for file_extension in file_extensions:
            files = self.zip_files_by_file_extension(cfg, file_extension)

    def zip_files_by_file_extension(self, cfg, file_extension):
        stem_files_list = cfg['file_management']['input_files'][file_extension]
        stem_list = [file.stem for file in stem_files_list]
        
        input_file_directory = cfg['analysis_settings']['directory']
        input_file_directory = 
        input_file_extenstions = cfg['analysis_settings']['file_extensions']
        for stem in stem_list:
            files = []
            for file in os.listdir(input_file_directory):
                for input_file_extension in input_file_extenstions:
                    if file.endswith(input_file_extension):
                        files.append(file)

            self.zip_files(files, stem)

    def zip_files(self, files, stem):
        with ZipFile(zip_name, 'w') as zip:
            for file in files:
                zip.write(file)

    def unzip_files(self, zip_name, destination):
        with ZipFile(zip_name, 'r') as zip:
            zip.extractall(destination)