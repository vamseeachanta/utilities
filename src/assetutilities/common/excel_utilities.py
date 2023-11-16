from xlsxwriter.workbook import Workbook
from xlsxwriter.utility import xl_rowcol_to_cell
from assetutilities.common.data import ReadFromExcel
from assetutilities.

rfe = ReadFromExcel()
cc = CustomCalculations()


class ExcelUtilities:

    def __init__(self) -> None:
        pass

    def excel_utility_router(self, cfg):
        if cfg['task'] == 'cross_reference_values_from_closed_workbooks':
            self.cross_reference_values_from_closed_workbooks_xlsxwriter(cfg)
        if cfg['task'] == 'custom_calculation':
            data = self.get_data(cfg)

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
            "'S:\Proj\\02_ANALYSIS\\2_DETAILED\\1.0 Mooring\\02 Pre-lay\\2. Dynamic\Report Tables\[S01-Dyn-FC180-2.5mHs.xlsx]EditingTable'!BH5"
        )

        # worksheet.write_formula(
        #     'A3', "'[S01-Dyn-FC180-2.5mHs.xlsx]EditingTable'!BH5")
        # worksheet.write_formula('A2',"=A20")

        # workbook.add_worksheet('Sheet2')

        workbook.close()

    def get_data(self, cfg):
        pass