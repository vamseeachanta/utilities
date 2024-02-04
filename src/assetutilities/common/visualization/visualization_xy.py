import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from assetutilities.common.visualization.visualization_common import VisualizationCommon

visualization_common = VisualizationCommon()


class VisualizationXY:

    def __init__(self):
        pass

    def xy_plot_set_up_and_save(self, cfg, plt_settings):
        data_df, cfg = self.get_xy_data(cfg)
        # if cfg['settings']['plt_engine'] == 'plotly':
        #     plt = self.get_xy_plot_plotly(data_df, plt_settings)
        #     self.save_xy_plot_and_close_plotly(plt, cfg)
        if cfg['settings']['plt_engine'] == 'matplotlib':
            plt_properties = self.get_xy_plot_matplotlib(
                data_df, plt_settings, cfg)
            self.save_xy_plot_and_close_matplotlib(plt_properties, cfg)
        else:
            raise ValueError('Invalid plt_engine')

    def get_xy_data(self, cfg):
        if cfg['data']['type'] == 'input':
            data_dict = self.get_xy_mapped_data_dict_from_input(cfg)
            data_df = pd.DataFrame.from_dict(data_dict,
                                             orient='index').transpose()
        elif cfg['data']['type'] == 'csv':
            data_dict, cfg = self.get_xy_mapped_data_dict_from_csv(cfg)
            data_df = pd.DataFrame.from_dict(data_dict,
                                             orient='index').transpose()

        return data_df, cfg

    def get_xy_mapped_data_dict_from_input(self, mapped_data_cfg):
        x_data = mapped_data_cfg['data']['x']
        y_data = mapped_data_cfg['data']['y']

        no_of_trends = max(len(x_data), len(y_data))

        if len(x_data) < len(y_data):
            x_data = [x_data[0]] * len(y_data)
        if len(x_data) > len(y_data):
            y_data = [y_data[0]] * len(x_data)

        data_dict = {}
        for i in range(0, no_of_trends):
            data_dict.update({'x_' + str(i): x_data[i]})
            data_dict.update({'y_' + str(i): y_data[i]})

        return data_dict

    def get_xy_mapped_data_dict_from_csv(self, cfg):
        mapped_data_cfg = {}
        x_data_array = []
        y_data_array = []

        legend_data = []
        for csv_cfg in cfg['data']['csv']:
            df = pd.read_csv(csv_cfg['file_name'])
            x_data_dict = df[csv_cfg['columns']['x']].to_dict('list')
            y_data_dict = df[csv_cfg['columns']['y']].to_dict('list')

            x_legend_array = []
            y_legend_array = []

            for x_column in csv_cfg['columns']['x']:
                x_data = x_data_dict[x_column]
                x_data_array = x_data_array + [x_data]

                legend_label = csv_cfg['label'] + ', ' + x_column
                x_legend_array.append(legend_label)

            for y_column in csv_cfg['columns']['y']:
                y_data = y_data_dict[y_column]
                y_data_array = y_data_array + [y_data]

                legend_label = csv_cfg['label'] + ', ' + y_column
                y_legend_array.append(legend_label)

            # Consolidate x and y data
            if len(csv_cfg['columns']['x']) <= len(csv_cfg['columns']['y']):
                legend_data = legend_data + y_legend_array
            else:
                legend_data = legend_data + x_legend_array

        if len(cfg['settings']['legend']['label']) == len(legend_data):
            legend_data = cfg['settings']['legend']['label']
            logging.info('Using legend labels from the input file')
        elif len(cfg['settings']['legend']['label']) > 0:
            logging.warning(
                'The number of legend labels is not equal to the number of data columns.'
            )
            logging.warning('Ignoring the legend labels in the input file')

        mapped_data_cfg = {'data': {'x': x_data_array, 'y': y_data_array}}
        cfg['settings']['legend']['label'] = legend_data
        data_dict = self.get_xy_mapped_data_dict_from_input(mapped_data_cfg)

        return data_dict, cfg

    def get_xy_plot_matplotlib(self, df, plt_settings, cfg):
        import matplotlib.pyplot as plt
        if 'plt_properties' in plt_settings and plt_settings['plt_properties'][
                'plt'] is not None:
            plt = plt_settings['plt_properties']['plt']

        fig, ax = plt.subplots()

        # Add trace or plot style
        plt_settings['traces'] = int(len(df.columns) / 2)
        for index in range(0, plt_settings['traces']):
            ax.plot(df['x_' + str(index)],
                    df['y_' + str(index)],
                    label=plt_settings['legend']['label'][index],
                    color=cfg['data']['color'][index],
                    linestyle=cfg['data']['linestyle'][index],
                    alpha=cfg['data']['alpha'][index])

        grid = plt_settings.get('grid', True)
        ax.grid(grid)

        title = plt_settings.get('title', None)
        if title is not None:
            ax.set_title(plt_settings['title'], va='bottom')

        legend_flag = plt_settings['legend'].get('flag', True)
        if legend_flag:
            ax.legend(loc='best')
            prop = plt_settings['legend'].get('prop', None)
            if prop is not None:
                plt.legend(prop=prop)

        plt_properties = {'plt': plt, 'fig': fig}
        if 'add_axes' in cfg and len(cfg.add_axes) > 0:
            self.add_axes_to_plt(plt_properties, cfg)

        ax.set(xlabel=plt_settings.get('xlabel', None),
               ylabel=plt_settings.get('ylabel', None))
        ax.label_outer()

        return {'plt': plt, 'fig': fig}

    def save_xy_plot_and_close_matplotlib(self, plt_properties, cfg):
        plot_name_paths = visualization_common.get_plot_name_path(cfg)
        plt = plt_properties['plt']
        for file_name in plot_name_paths:
            plt.savefig(file_name, dpi=800)

    def resolve_legends(self):
        # TODO Resolve legends in a comprehensive manner
        # Get legend data
        if 'legend' in mapped_data_cfg['data']:
            legend_data = mapped_data_cfg['data']['legend']
        elif 'legend_data' in mapped_data_cfg:
            legend_data = mapped_data_cfg['legend_data']
        else:
            legend_data = []

        no_of_trends = max(len(x_data), len(y_data))

        if not len(legend_data) == no_of_trends:
            legend_data = ['legend_' + str(i) for i in range(0, no_of_trends)]
