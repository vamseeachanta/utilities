import glob


class FileManagement:

    def __init__(self) -> None:
        pass

    def fm_router(self, cfg):
        self.get_files_in_directory(cfg)


    def get_files_in_directory(self, cfg):
        if cfg['files']['files_in_current_directory']['flag']:
            file_folder = cfg['Analysis']['analysis_root_folder']
        else:
            file_folder = cfg['files']['files_in_current_directory']['directory']

        extension = cfg['files']['extension']
        files = glob.glob(file_folder+'\*.' + extension)

        cfg.update({cfg['basename']: {'files': files}})

        return cfg
