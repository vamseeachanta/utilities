# import camelot
import tabula


class ReadPDF:

    def __init__(self) -> None:
        pass

    def read_pdf(self, cfg, file_index=0):
        if cfg['files']['from_pdf'][file_index].__contains__('package'):
            if cfg['files']['from_pdf'][file_index]['package'] in [
                    None, 'tabula'
            ]:
                df = self.from_pdf_tabula(cfg, file_index)
            elif cfg['files']['from_pdf'][file_index]['package'] == 'camelot':
                df = self.from_pdf_camelot(cfg, file_index)
        else:
            df = self.from_pdf_tabula(cfg, file_index)

        return df

    def from_pdf_tabula(self, cfg, file_index=0):
        df = tabula.read_pdf(cfg['files']['from_pdf'][file_index]['io'],
                             pages=cfg['files']['from_pdf'][file_index]['page'],
                             multiple_tables=True)
        return df

    def from_pdf_camelot(self, cfg, file_index=0):
        df = camelot.read_pdf(
            cfg['files']['from_pdf'][file_index]['io'],
            pages=cfg['files']['from_pdf'][file_index]['page'],
            suppress_stdout=False)
        print(df)
        return df
