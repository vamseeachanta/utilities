import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class VisualizationCommon:

    def __init__(self):
        pass

    def add_legend(self, plt, plt_settings):
        if plt_settings.__contains__('legend') and plt_settings['legend']:
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
        self.add_markers
        self.save_and_close()

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

    def get_plot_name_path(self, cfg):
        file_name = cfg['settings']['file_name']
        if file_name is None:
            file_name = cfg['Analysis']['file_name']
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

    def get_colors(self, set='single', n=15):
        '''
        https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm
        '''
        from webcolors import rgb_to_hex

        if set == 'single':
            if n <= 10:
                colors = [
                    "#17becf", "#bcbd22", "#7f7f7f", "#e377c2", "#8c564b",
                    "#9467bd", "#d62728", "#2ca02c", "#ff7f0e", "#1f77b4"
                ]
            else:
                colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14),
                          (255, 187, 120), (44, 160, 44), (152, 223, 138),
                          (214, 39, 40), (255, 152, 150), (148, 103, 189),
                          (197, 176, 213), (140, 86, 75), (196, 156, 148),
                          (227, 119, 194), (247, 182, 210), (127, 127, 127),
                          (199, 199, 199), (188, 189, 34), (219, 219, 141),
                          (23, 190, 207), (158, 218, 229)]
                colors = [rgb_to_hex(color) for color in colors]
        elif set == 'multi':
            if n <= 8:
                color_1 = ["#0F6BE9", "#043F8F", "#001E45"]
                color_2 = ["#D1350A", "#B23000", "#2F1202"]
                color_3 = ["#A06900", "#5D4101", "#2C1B07"]
                color_4 = ["#05B25D", "#044B32", "#012B1"]
                color_5 = ["#A37BFA", "#492D99", "#019OA52"]
                color_6 = ["#017C9D", "#D1485B", "#062530"]
                color_7 = ["#D2186D", "#880C3E", "#3A0116"]
                color_8 = ["#DC1830", "#830A12", "#340301"]

                set1 = [
                    color_1[0], color_2[0], color_3[0], color_4[0], color_5[0],
                    color_6[0], color_7[0], color_8[0]
                ]
                set2 = [
                    color_1[1], color_2[1], color_3[1], color_4[1], color_5[1],
                    color_6[1], color_7[1], color_8[1]
                ]
                set3 = [
                    color_1[2], color_2[2], color_3[2], color_4[2], color_5[2],
                    color_6[2], color_7[2], color_8[2]
                ]
                set1 = [rgb_to_hex(color) for color in set1]
                set2 = [rgb_to_hex(color) for color in set2]
                set3 = [rgb_to_hex(color) for color in set3]
                colors = {'set1': set1, 'set2': set2, 'set3': set3}
            else:
                raise ValueError('Number of colors must be less than 9')
        return colors

    def marker_settings(self, plt_settings):
        
        markerfacecolor = None
        markersize = None
        if plt_settings.__contains__('marker'):
            if (plt_settings['marker'] is not None) and (plt_settings['marker'].__contains__('edge_color')):
                markerfacecolor = plt_settings['marker']['edge_color']
            if plt_settings.__contains__('color'):
                markerfacecolor = plt_settings['color']
            if plt_settings['marker'] is not None and plt_settings['marker'].__contains__('size'):
                markersize = plt_settings['marker']['size']
            else:
                markersize = 2

        marker_settings = {'markerfacecolor': markerfacecolor, 'markersize': markersize}

        return marker_settings