import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from assetutilities.common.visualization.visualization_xy import VisualizationXY
from assetutilities.common.update_deep import update_deep_dictionary

class VisualizationComponents():
    # https://plot.ly/python/v3/fft-filters/
    # http://scipy-lectures.org/intro/scipy/auto_examples/plot_fftpack.html
    # https://dsp.stackexchange.com/questions/724/low-pass-filter-and-fft-for-beginners-with-python

    def __init__(self, cfg=None):
        self.cfg = cfg

    def visualization_router(self, cfg):

        cfg = self.get_cfg_with_master_data(cfg)

        plt_settings = cfg['settings']
        if 'polar' in cfg['settings']['type']:
            self.polar_plot_set_up(cfg, plt_settings)
        elif 'xy' in cfg['settings']['type']:
            visualization_xy = VisualizationXY()
            visualization_xy.xy_plot_set_up_and_save(cfg, plt_settings)
        else:
            raise (Exception(f'Other plots coding to be completed ... FAIL'))


    def get_cfg_with_master_data(self, cfg):
        if 'master_settings' in cfg:
            master_settings = cfg['master_settings'].copy()
            data_settings = cfg['data']

            for group_index in range(0, len(data_settings['groups'])):
                group = data_settings['groups'][group_index].copy()
                group = update_deep_dictionary(master_settings['groups'], group)
                data_settings['groups'][group_index] = group.copy()

        return cfg

