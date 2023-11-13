import glob


class FileManagement:

    def __init__(self) -> None:
        pass

    def get_files_in_directory(self, folder=None):
        simfs = glob.glob('*.sim')
