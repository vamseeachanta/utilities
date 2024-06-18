import os
import itertools
import shutil
import pathlib

from assetutilities.common.file_management import FileManagement

from assetutilities.common.file_edit_concatenate import FileConcatenate
from assetutilities.common.file_edit_split import FileSplit

fm = FileManagement()
fe_c = FileConcatenate()
fe_s = FileSplit()


class FileEdit:

    def __init__(self) -> None:
        pass

    def router(self, cfg):
        cfg = self.file_management(cfg)
        if cfg["edit_type"] == "concatenate":
            fe_c.concatenate_files(cfg)
        elif cfg["edit_type"] == "split":
            fe_s.router(cfg)

    def file_management(self, cfg):
        cfg = fm.router(cfg)

        return cfg
