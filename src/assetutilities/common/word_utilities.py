# Standard library imports

# Standard library imports
from re import search

# Third party imports
from docx import Document, opendocx

# from docx import opendocx


class WordUtilities:

    def __init__(self):
        pass

    def router(self, cfg):
        if cfg.task == "search_strings":
            self.search_strings(cfg)
        elif cfg.task == "csv_to_docx":
            self.csv_to_docx(cfg)
        else:
            raise ValueError("Task not found in WorkUtilities")

    def search_strings(self, cfg):
        document_name = cfg["files"]["file_name"]
        document_data = Document(document_name)
        search_string = None
        for paragraph in document_data.paragraphs:
            if search_string in paragraph.text:
                print(True)

        # Open the .docx file
        document = opendocx("A document.docx")

        # Search returns true if found
        search(document, "your search string")

    def csv_to_docx(self, cfg):
        pass
        # CODE GOES HERE