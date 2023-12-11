import glob


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
        files = glob.glob(file_folder+'\*.' + extension)

        cfg_filter = cfg['files']['filters']
        filtered_files =self.get_filtered_files(files, cfg_filter)

        cfg.update({cfg['basename']: {'files': filtered_files}})

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