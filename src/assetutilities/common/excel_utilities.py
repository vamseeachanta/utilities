import os
import excel2img

from xlsxwriter.workbook import Workbook
from xlsxwriter.utility import xl_rowcol_to_cell

from assetutilities.common.data import ReadFromExcel
from assetutilities.calculations.polynomial import Polynomial


rfe = ReadFromExcel()
_polynomial = Polynomial()


class ExcelUtilities:

    def __init__(self) -> None:
        pass

    def router(self, cfg):
        if cfg['task'] == 'cross_reference_values_from_closed_workbooks':
            self.cross_reference_values_from_closed_workbooks_xlsxwriter(cfg)
        if cfg['task'] == 'custom_calculation':
            data = self.get_data(cfg)

        return cfg
    
    def excel_utility_router(self, cfg):
        if cfg['task'] == 'cross_reference_values_from_closed_workbooks':
            self.cross_reference_values_from_closed_workbooks_xlsxwriter(cfg)
        if cfg['task'] == 'custom_calculation':
            data = self.get_data(cfg)
        if cfg['task'] == 'excel_to_image':
            data = self.excel_to_image(cfg)


        return cfg

    def cross_reference_values_from_closed_workbooks_xlsxwriter(self, cfg):

        workbook = Workbook(cfg['files']['target']['path'] +
                            cfg['files']['target']['workbook'])
        worksheet = workbook.add_worksheet(cfg['files']['target']['worksheet'])
        worksheet.write_formula('A2',
                                "=VLOOKUP(B3,'Sheet2'!$B$2:$R$2199,17,FALSE)")

        cell_range = xl_rowcol_to_cell(4, 1)
        cell_formula = cfg['files']['source']['path'] + "[" + cfg['files'][
            'source']['workbook'] + "]" + cfg['files']['source'][
                'worksheet'] + "!" + "BH5"
        # TODO did not work with abstraction
        # worksheet.write_formula(cell_range, cell_formula)

        worksheet.write_formula(
            'A3',
            "[S01-Dyn-FC180-2.5mHs.xlsx]EditingTable'!BH5"
        )

        # worksheet.write_formula(
        #     'A3', "'[S01-Dyn-FC180-2.5mHs.xlsx]EditingTable'!BH5")
        # worksheet.write_formula('A2',"=A20")

        # workbook.add_worksheet('Sheet2')

        workbook.close()

    def get_data(self, cfg):
        pass

    def excel_to_image(self, cfg):

        for file in cfg['files']:
            io = file['io']
            for sheetname in file['sheet_name']:
                for array_range in file['range']:
                    cell_range = array_range[0] + ":" + array_range[1]
                    sheet_range = sheetname + "!" + cell_range
                    output_basename = sheetname + "_" + array_range[0] + array_range[1]
                    for ext in file['output_extension']:
                        output_filename = output_basename + "." + ext
                        if file['output_dir'] is not None and os.path.isdir(file['output_dir']):
                            output_filename = os.path.join(file['output_dir'], output_filename)
                        else:
                            output_filename = os.path.join(cfg['Analysis']['result_folder'], output_filename)
                        excel2img.export_img(io, output_filename, "", sheet_range)
