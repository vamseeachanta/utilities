import PyPDF2


class EditPDF:

    def __init__(self) -> None:
        pass

    def edit_pdf(self, cfg, file_index=0):
        parse_library = cfg.get('library', 'PyPDF2')
        if parse_library == 'PyPDF2':
            self.from_pdf_PyPDF2(cfg, file_index)
        else:
            raise KeyError("PDF library not programmed")

    def from_pdf_PyPDF2(self, cfg, file_index=0):

        file_name = cfg['files'][file_index]['io']
        pages_groups = cfg['files'][file_index]['pages']

        pdf_reader = PyPDF2.PdfReader(file_name)

        for pages in pages_groups:
            pdf_writer = PyPDF2.PdfWriter()
            page_range = range(pages[0], pages[1] + 1)

            for page_num, page in enumerate(pdf_reader.pages, 1):
                if page_num in page_range:
                    pdf_writer.add_page(page)

            with open(f'{file_name}_page_{pages[0]}-{pages[1]}.pdf',
                      'wb') as out:
                pdf_writer.write(out)

            print(f'Created: {file_name}_page_{pages[0]}-{pages[1]}.pdf')

        #TODO Add results to cfg for tests
