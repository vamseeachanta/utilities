# Reader imports
from assetutilities.common.data import AttributeDict
from assetutilities.common.yml_utilities import WorkingWithYAML

wwy = WorkingWithYAML()


class VisualizationTemplates:

    def __init__(self):
        pass

<<<<<<< HEAD
    def get_xy_plot_yml_input(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
            'filename': 'tests/test_data/visualization/xy_line_matplotlib_input.yml',
=======
    def get_xy_scatter_input(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
            'filename': 'base_configs/modules/visualization/template_xy_scatter_input.yml',
            'library_name': library_name
        }
        plot_template = wwy.get_library_yaml_file(library_yaml_cfg)
        plot_template['Analysis'] = custom_analysis_dict
        plot_template = AttributeDict(plot_template)

        return plot_template

    def get_xy_line_input(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
            'filename': 'base_configs/modules/visualization/template_xy_line_input.yml',
>>>>>>> main
            'library_name': library_name
        }
        plot_template = wwy.get_library_yaml_file(library_yaml_cfg)
        plot_template['Analysis'] = custom_analysis_dict
        plot_template = AttributeDict(plot_template)

        return plot_template

    def get_xy_scatter_csv(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
<<<<<<< HEAD
            'filename': 'tests/test_data/visualization/template_xy_scatter_csv.yml',
=======
            'filename': 'base_configs/modules/visualization/template_xy_scatter_csv.yml',
>>>>>>> main
            'library_name': library_name
        }
        plot_template = wwy.get_library_yaml_file(library_yaml_cfg)
        plot_template['Analysis'] = custom_analysis_dict
        plot_template = AttributeDict(plot_template)

        return plot_template

<<<<<<< HEAD
    def get_xy_plot_line_csv(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
            'filename': 'tests/test_data/visualization/template_xy_line_csv.yml',
=======
    def get_xy_line_csv(self, custom_analysis_dict={}):
        library_name = 'assetutilities'
        library_yaml_cfg = {
            'filename': 'base_configs/modules/visualization/template_xy_line_csv.yml',
>>>>>>> main
            'library_name': library_name
        }
        plot_template = wwy.get_library_yaml_file(library_yaml_cfg)
        plot_template['Analysis'] = custom_analysis_dict
        plot_template = AttributeDict(plot_template)

        return plot_template
