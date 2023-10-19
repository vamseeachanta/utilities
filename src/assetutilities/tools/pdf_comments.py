import poppler
import sys
import urllib
import os

# https://stackoverflow.com/questions/1106098/parse-annotations-from-a-pdf


class PDFComments:

    def __init__(self):
        pass

    def method_1(
        self,
        filename='C:/Users/ss7a2365/Desktop/VST-VK912-ENG-RPT-SS7-00016-00 DP & AMACD Comments.pdf'
    ):

        document = poppler.document_new_from_file(filename, None)
        n_pages = document.get_n_pages()
        all_annots = 0

        for i in range(n_pages):
            page = document.get_page(i)
            annot_mappings = page.get_annot_mapping()
            num_annots = len(annot_mappings)
            if num_annots > 0:
                for annot_mapping in annot_mappings:
                    if annot_mapping.annot.get_annot_type(
                    ).value_name != 'POPPLER_ANNOT_LINK':
                        all_annots += 1
                        print(
                            'page: {0:3}, {1:10}, type: {2:10}, content: {3}'.
                            format(
                                i + 1, annot_mapping.annot.get_modified(),
                                annot_mapping.annot.get_annot_type().value_nick,
                                annot_mapping.annot.get_contents()))

        if all_annots > 0:
            print(str(all_annots) + " annotation(s) found")
        else:
            print("no annotations found")


if __name__ == "__main__":
    pdf_comments = PDFComments()
    pdf_comments.method_1()