import os
import glob
import pathlib

class FileManagement:

    def __init__(self) -> None:
        pass

    def router(self, cfg):
        self.get_files_in_directory(cfg)


    def get_files_in_directory(self, cfg):
        if cfg['files']['files_in_current_directory']['flag']:
            file_folder = cfg['Analysis']['analysis_root_folder']
        else:
            file_folder = cfg['files']['files_in_current_directory']['directory']

        extension = cfg['files']['extension']
        os.path.join(file_folder,'*.' + extension)
        files = glob.glob(os.path.join(file_folder,'*.' + extension))

        if 'filters' in cfg['files']:
            cfg_filter = cfg['files']['filters']
            filtered_files =self.get_filtered_files(files, cfg_filter)
        else:
            filtered_files = files.copy()

        basenames = self.get_basenames(filtered_files)
        cfg.update({cfg['basename']: {'files': filtered_files, 'basenames': basenames, 'file_folder': file_folder}})

        return cfg

    def get_filtered_files(self, files, cfg_filter):
        filtered_files = files.copy()
        for file in filtered_files:
            filter_flag = False
            if len(cfg_filter['filename_contains']) > 0 and not cfg_filter['filename_contains'][0] in file:
                filter_flag = True
            if len(cfg_filter['filename_not_contains']) > 0 and cfg_filter['filename_not_contains'][0] in file:
                filter_flag = True

            if filter_flag: 
                filtered_files.remove(file)

        return filtered_files
    
    def get_basenames(self, files):
        basenames = []
        for file in files:
            basenames.append(os.path.basename(file))
        return basenames
    
    def get_filename_without_extension(self, filename):

        basename = os.path.splitext(os.path.basename(filename))[0]
        filename_path = pathlib.Path(filename).parent
        filename_with_path = os.path.join(filename_path, basename)
        
        filename_without_extension = {'without_path': basename, 'with_path': filename_with_path}

        return filename_without_extension