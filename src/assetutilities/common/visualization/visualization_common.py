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
