# Standard library imports
import logging
import os
import sys

# Reader imports
from assetutilities.common.ApplicationManager import ConfigureApplicationInputs
from assetutilities.common.data import SaveData
from assetutilities.common.data_exploration import DataExploration
from assetutilities.common.excel_utilities import ExcelUtilities
from assetutilities.common.file_edit import FileEdit
from assetutilities.common.file_management import FileManagement
from assetutilities.common.text_analytics import TextAnalytics
from assetutilities.common.update_deep import AttributeDict
from assetutilities.common.utilities import save_application_cfg
from assetutilities.common.visualization_components import VisualizationComponents
from assetutilities.common.word_utilities import WordUtilities
from assetutilities.common.yml_utilities import ymlInput
from assetutilities.tools.git.git_python_utilities import GitPythonUtilities
from assetutilities.tools.pdf.edit_pdf import EditPDF
from assetutilities.tools.pdf.read_pdf import ReadPDF

library_name = "assetutilities"

de = DataExploration()
fm = FileManagement()
save_data = SaveData()


def engine(inputfile: str = None, cfg: dict = None) -> dict:
    fm = FileManagement()
    if cfg is None:
        inputfile = validate_arguments_run_methods(inputfile)
        cfg = ymlInput(inputfile, updateYml=None)
        cfg = AttributeDict(cfg)
        if cfg is None:
            raise ValueError("cfg is None")

    basename = cfg["basename"]
    application_manager = ConfigureApplicationInputs(basename)
    application_manager.configure(cfg, library_name)
    cfg_base = application_manager.cfg
    cfg_base = fm.router(cfg_base)

    logging.info(f"{basename}, application ... START")

    if basename in ["excel_utilities"]:
        eu = ExcelUtilities()
        cfg_base = eu.excel_utility_router(cfg_base)
    elif basename in ["visualization"]:
        viz_comp = VisualizationComponents()
        viz_comp.visualization_router(cfg_base)
    elif basename in ["read_pdf"]:
        read_pdf = ReadPDF()
        read_pdf.read_pdf(cfg_base)
    elif basename in ["file_management"]:
        fm = FileManagement()
        fm.router(cfg_base)
    elif basename in ["file_edit"]:
        fe = FileEdit()
        fe.router(cfg_base)
    elif basename in ["edit_pdf"]:
        edit_pdf = EditPDF()
        edit_pdf.edit_pdf(cfg_base)
    elif basename in ["gitpython"]:
        gpu = GitPythonUtilities()
        gpu.router(cfg_base)
    elif basename in ["text_analytics"]:
        ta = TextAnalytics()
        ta.router(cfg_base)
    elif basename in ["word_utilities"]:
        wu = WordUtilities()
        wu.router(cfg_base)
    elif cfg["basename"] == "data_exploration":
        cfg_base = de.router(cfg_base)
    
    else:
        raise (Exception(f"Analysis for basename: {basename} not found. ... FAIL"))

    if cfg is None:
        save_application_cfg(cfg_base=cfg_base)

    logging.info(f"{basename}, application ... END")


    return cfg_base


def validate_arguments_run_methods(inputfile):
    """
    Validate inputs for following run methods:
    - module (i.e. python -m digitalmodel input.yml)
    - from python file (i.e. )
    """

    if len(sys.argv) > 1 and inputfile is not None:
        raise (
            Exception(
                "2 Input files provided via arguments & function. Please provide only 1 file ... FAIL"
            )
        )

    if len(sys.argv) > 1:
        if not os.path.isfile(sys.argv[1]):
            raise (FileNotFoundError(f"Input file {sys.argv[1]} not found ... FAIL"))
        else:
            inputfile = sys.argv[1]

    if len(sys.argv) <= 1:
        if not os.path.isfile(inputfile):
            raise (FileNotFoundError(f"Input file {inputfile} not found ... FAIL"))
        else:
            sys.argv.append(inputfile)
    return inputfile


def save_cfg(cfg_base):
    output_dir = cfg_base.Analysis["result_folder"]

    filename = cfg_base.Analysis["file_name"]
    filename_path = os.path.join(output_dir, filename)

    save_data.saveDataYaml(cfg_base, filename_path, default_flow_style=False)
