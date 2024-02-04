import logging
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from assetutilities.common.visualization.visualization_xy import VisualizationXY

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
            visualization_xy = VisualizationXY()
            visualization_xy.xy_plot_set_up_and_save(cfg, plt_settings)
        else:
            raise (Exception(f'Other plots coding to be completed ... FAIL'))



