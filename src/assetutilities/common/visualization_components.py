import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class VisualizationComponents():
    # https://plot.ly/python/v3/fft-filters/
    # http://scipy-lectures.org/intro/scipy/auto_examples/plot_fftpack.html
    # https://dsp.stackexchange.com/questions/724/low-pass-filter-and-fft-for-beginners-with-python

    def __init__(self, cfg=None):
        self.cfg = cfg

    def visualization_router(self, cfg):
        plt_settings = cfg['settings']
        if 'polar' in cfg['settings']['plt_kind']:
            self.polar_plot_set_up(cfg, plt_settings)
        elif 'xy' in cfg['settings']['plt_kind']:
            self.xy_plot_set_up(cfg, plt_settings)
        else:
            raise (Exception(f'Other plots coding to be completed ... FAIL'))

    def xy_plot_set_up(self, cfg, plt_settings):
        data_df = self.get_xy_data(cfg)
        if cfg['settings']['plt_engine'] == 'plotly':
            plt = self.get_xy_plot_plotly(data_df, plt_settings)
            self.save_xy_plot_and_close_plotly(plt, cfg)
        elif cfg['settings']['plt_engine'] == 'matplotlib':
            plt_properties = self.get_xy_plot_matplotlib(data_df, plt_settings, cfg)
            self.save_xy_plot_and_close_matplotlib(plt_properties, cfg)

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

    def get_xy_data(self, cfg):
        if cfg['data']['type'] == 'input':
            data_dict = self.get_xy_mapped_data_dict(cfg)
            data_df = pd.DataFrame.from_dict(data_dict, orient='index').transpose()
        elif cfg['data']['type'] == 'csv':
            data_dict = self.get_xy_from_csv(cfg)
        
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

    def get_xy_mapped_data_dict(self, cfg):
        x_data = cfg['data']['x']
        y_data = cfg['data']['y']
        
        # Get legend data
        if 'legend' in cfg['data']:
            legend_data = cfg['data']['legend']
        else:
            legend_data = []
            
        no_of_trends = max(len(x_data), len(y_data))
        
        if not len(legend_data) == no_of_trends:
            legend_data = ['legend_' + str(i) for i in range(0, no_of_trends)]
            
        if len(x_data) < len(y_data):
            x_data = [x_data[0]] * len(y_data)
        if len(x_data) > len(y_data):
            y_data = [y_data[0]] * len(x_data)

        data_dict = {}
        for i in range(0, len(legend_data)):
            data_dict.update({'x_' + str(i): x_data[i]})
            data_dict.update({'y_' + str(i): y_data[i]})

        return data_dict

    def get_xy_from_csv(self, cfg):
        pass
    
    def get_data_from_csv(self, cfg):
        pass
    
    def get_axis_for_polar(self, rect):
        rect_polar = rect.copy()
        rect_polar[0] = rect[0] * np.pi / 180
        rect_polar[1] = rect[1] * np.pi / 180

        return rect_polar


    def add_legend(self, plt, plt_settings):
        if plt_settings.__contains__(
                'legend') and plt_settings['legend']:
            if plt_settings.__contains__('legend_location'):
                legend_location = plt_settings['legend_location']
            else:
                legend_location = None

            if legend_location == "lower center":
                plt.legend(loc='best', fontsize=8)
            elif (legend_location is None) or (legend_location == "best"):
                plt.legend(loc='best', fontsize=8)
                
        return plt

    def future_functions(self):
        # TODO
        self.add_title_and_axis_labels()
        self.add_legend()
        self.add_x_y_lim_formats()
        self.add_reference_lines_and_spans()
        self.save_and_close()

    def get_polar_plot_plotly(self, df, plt_settings):
        if plt_settings['plt_kind'] == 'polar':
            # Radial line

            plt.polar(df['x'], df['y'], label=plt_settings['label'])
        elif plt_settings['plt_kind'] == 'polar_scatter':
            # Radial scatter
            import plotly.express as px
            plt = px.scatter_polar(df, r=df['r_0'], theta=df['theta_0'])

        return plt

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

    def add_axes_to_plt(self, plt_properties, cfg):
        for axes_idx in range(0, len(cfg.add_axes)):
            cfg_plt = cfg.add_axes[axes_idx]
            plt_settings = cfg_plt['settings']
            plt_settings.update({'add_axes': True})
            plt_settings.update({'plt_properties': plt_properties})

            data_df = self.get_polar_data(cfg_plt)
            plt_settings['traces'] = int(len(data_df.columns) / 2)

            plt = self.get_polar_plot_matplotlib(data_df, plt_settings, cfg_plt)

    def get_plt_with_arrows(self, plt, plt_settings):

        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.arrow.html
        # Add arrows with direct data
        # Try inset_axes: https://matplotlib.org/2.0.2/examples/pylab_examples/axes_demo.html
        if not 'arrows' in plt_settings:
            return plt

        arrows = plt_settings['arrows']
        for arrow in arrows:
            # arr1 = plt.arrow(3, 0, 5, 45, color='blue')
            # # arrow at 45 degree
            theta = arrow['theta']
            r = arrow['r']
            color = arrow['color']

            arr = plt.arrow(theta[0] / 180. * np.pi,
                            r[0],
                            theta[1] / 180. * np.pi,
                            r[1] - r[0],
                            alpha=0.75,
                            width=0.015,
                            color=color,
                            lw=2,
                            zorder=5)

        return plt

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

    def save_xy_plot_and_close_matplotlib(self, plt_properties, cfg):
        plot_name_paths = self.get_plot_name_path(cfg)
        plt = plt_properties['plt']
        for file_name in plot_name_paths:
            plt.savefig(file_name, dpi=800)

    def get_plot_name_path(self, cfg):
        file_name = cfg['settings']['file_name']
        extensions = cfg['settings']['plt_save_extensions']
        plot_folder = os.path.join(cfg['Analysis']['result_folder'], 'Plot')

        plot_name_paths = [
            os.path.join(plot_folder, file_name + extension)
            for extension in extensions
        ]

        return plot_name_paths

    def add_annotations(self):
        '''
        https://matplotlib.org/stable/gallery/text_labels_and_annotations/annotation_demo.html
        #TODO abstract annotation and move to another function.
        or use graphics?
        '''
        ax.annotate(
            'a polar annotation',
            xy=(30, 5),    # theta, radius
            xytext=(0.05, 0.05),    # fraction, fraction
            textcoords='figure fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left',
            verticalalignment='bottom')
