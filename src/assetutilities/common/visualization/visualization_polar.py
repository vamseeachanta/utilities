import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class VisualizationPolar:

    def __init__(self):
        pass

    def polar_plot_set_up(self, cfg, plt_settings):
        data_df = self.get_polar_data(cfg)
        plt_settings['traces'] = int(len(data_df.columns) / 2)
        if cfg['settings']['plt_engine'] == 'plotly':
            plt = self.get_polar_plot_plotly(data_df, plt_settings)
            self.save_polar_plot_and_close_plotly(plt, cfg)
        elif cfg['settings']['plt_engine'] == 'matplotlib':
            plt_properties = self.get_polar_plot_matplotlib(
                    data_df, plt_settings, cfg)
            self.save_polar_plot_and_close_matplotlib(plt_properties, cfg)

    def get_polar_data(self, cfg):
        data_dict = self.get_polar_mapped_data_dict(cfg)
        data_df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
        return data_df


    def get_polar_mapped_data_dict(self, cfg):
        theta_data = cfg['data']['theta']
        r_data = cfg['data']['r']

        # Get legend data
        if 'legend' in cfg['data']:
            legend_data = cfg['data']['legend']
        else:
            legend_data = []

        no_of_trends = max(len(theta_data), len(r_data))
        if not len(legend_data) == no_of_trends:
            legend_data = ['legend_' + str(i) for i in range(0, no_of_trends)]

        if len(theta_data) < len(r_data):
            theta_data = [theta_data[0]] * len(r_data)
        if len(theta_data) > len(r_data):
            r_data = [r_data[0]] * len(theta_data)

        for theta_index in range(0, len(theta_data)):
            new_data = [
                theta * np.pi / 180 for theta in theta_data[theta_index]
            ]
            theta_data[theta_index] = new_data

        data_dict = {}
        for i in range(0, len(legend_data)):
            data_dict.update({'r_' + str(i): r_data[i]})
            data_dict.update({'theta_' + str(i): theta_data[i]})

        return data_dict

    def get_axis_for_polar(self, rect):
        rect_polar = rect.copy()
        rect_polar[0] = rect[0] * np.pi / 180
        rect_polar[1] = rect[1] * np.pi / 180

        return rect_polar

    def get_polar_plot_plotly(self, df, plt_settings):
        if plt_settings['plt_kind'] == 'polar':
            # Radial line

            plt.polar(df['x'], df['y'], label=plt_settings['label'])
        elif plt_settings['plt_kind'] == 'polar_scatter':
            # Radial scatter
            import plotly.express as px
            plt = px.scatter_polar(df, r=df['r_0'], theta=df['theta_0'])

        return plt


    def get_polar_plot_matplotlib(self, df, plt_settings, cfg):

        import matplotlib.pyplot as plt
        if 'plt_properties' in plt_settings and plt_settings['plt_properties'][
                'plt'] is not None:
            plt = plt_settings['plt_properties']['plt']

        # Add axis for plot

        alpha = plt_settings.get('alpha', 1)
        facecolor = plt_settings.get('facecolor', None)
        if (not 'add_axes' in plt_settings) or (not plt_settings['add_axes']):
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'},
                                   facecolor=facecolor,
                                   alpha=alpha)
        else:
            fig = plt_settings['plt_properties']['fig']
            rect = plt_settings['rect']
            ax = fig.add_axes(rect,
                              polar=True,
                              facecolor=facecolor,
                              alpha=alpha)

            axis = plt_settings['axis']
            if axis != 'off':
                axis = self.get_axis_for_polar(axis)
            plt.axis(axis)

        # Add trace or plot style
        for index in range(0, plt_settings['traces']):
            if plt_settings['plt_kind'][index] == 'polar':
                ax.plot(df['theta_' + str(index)],
                        df['r_' + str(index)],
                        label=plt_settings['legend']['label'][index],
                        color=cfg['data']['color'][index],
                        linestyle=cfg['data']['linestyle'][index],
                        alpha=cfg['data']['alpha'][index])
            elif plt_settings['plt_kind'][index] == 'polar_scatter':
                ax.scatter(df['theta_' + str(index)],
                           df['r_' + str(index)],
                           label=plt_settings['legend']['label'][index],
                           color=cfg['data']['color'][index],
                           linestyle=cfg['data']['linestyle'][index],
                           alpha=cfg['data']['alpha'][index])

        legend_flag = plt_settings['legend'].get('flag', True)
        if legend_flag:
            ax.legend(loc='best')
            prop = plt_settings['legend'].get('prop', None)
            if prop is not None:
                plt.legend(prop=prop)

        plt = self.get_plt_with_arrows(plt, plt_settings)

        set_rmax = plt_settings.get('set_rmax', None)
        if set_rmax is not None:
            ax.set_rmax(set_rmax)

        set_rticks = plt_settings.get('set_rticks', None)
        if set_rticks is not None:
            ax.set_rticks(set_rticks)

        set_rlabel_position = plt_settings.get('set_rlabel_position', None)
        if set_rlabel_position is not None:
            ax.set_rlabel_position(set_rlabel_position)

        set_thetagrids = plt_settings.get('set_thetagrids', None)
        if set_thetagrids is not None:
            ax.set_thetagrids(set_thetagrids)

        set_theta_zero_location = plt_settings.get('set_theta_zero_location',
                                                   None)
        if set_theta_zero_location is not None:
            ax.set_theta_zero_location(set_theta_zero_location)

        grid = plt_settings.get('grid', True)
        ax.grid(grid)

        title = plt_settings.get('title', None)
        if title is not None:
            ax.set_title(plt_settings['title'], va='bottom')

        plt_properties = {'plt': plt, 'fig': fig}
        if 'add_axes' in cfg and len(cfg.add_axes) > 0:
            self.add_axes_to_plt(plt_properties, cfg)

        return {'plt': plt, 'fig': fig}

    def save_polar_plot_and_close_plotly(self, plt, cfg):
        plot_name_paths = self.get_plot_name_path(cfg)
        for file_name in plot_name_paths:
            # plt.write_image(file_name)
            plt.write_html(file_name)

            plt.savefig(file_name, dpi=100)

        plt.close()

    def save_polar_plot_and_close_matplotlib(self, plt_properties, cfg):
        plot_name_paths = self.get_plot_name_path(cfg)

        plt = plt_properties['plt']
        for file_name in plot_name_paths:
            plt.savefig(file_name, dpi=800)
