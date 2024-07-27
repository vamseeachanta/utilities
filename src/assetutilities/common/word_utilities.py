from re import search

import docx

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import pandas as pd
import os

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
        #document = opendocx("A document.docx")

        # Search returns true if found

    def csv_to_docx(self, cfg):
        input_csv = cfg['files']['file_name']

        # Read the CSV file as DataFrame
        df = pd.read_csv(input_csv)

        # Create a new Document
        doc = Document()

        # Add a table to the Document
        table = doc.add_table(rows=1, cols=len(df.columns))
        table.style = 'Table Grid'

        # Format the header row
        hdr_cells = table.rows[0].cells
        for i, column_name in enumerate(df.columns):
            hdr_cells[i].text = column_name
            hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
            hdr_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Add the rows to the table
        for index, row in df.iterrows():
            row_cells = table.add_row().cells
            for i, cell in enumerate(row):
                row_cells[i].text = str(cell)
                row_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
                row_cells[i].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Save the document
        output_docx = input_csv.replace(".csv", ".docx")
        doc.save(output_docx)
        print(f"CSV file has been converted to DOCX file ")
