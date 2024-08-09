# Third party imports
import matplotlib.pyplot as plt  # noqa
import numpy as np
from matplotlib import gridspec
from PIL import Image


def add_image_to_polar_plot(image_path, r_min, r_max, theta_min_deg, theta_max_deg, alpha):
    """
    Add an image to a polar plot with specified parameters.

    """
    theta_min = np.deg2rad(theta_min_deg)
    theta_max = np.deg2rad(theta_max_deg)

    im = Image.open(image_path)

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # fig, ax = plt.subplots()
    fig = plt.figure()

    spec = gridspec.GridSpec(ncols=1, nrows=2,
                            width_ratios=[1], wspace=0.5,
                            hspace=0.5, height_ratios=[1, 4])
 

    ax0 = fig.add_subplot(spec[0])
    ax1 = fig.add_subplot(spec[1], projection='polar')

    # ax1 = plt.subplot(122, projection='polar')

    extent = [theta_min, theta_max, r_min, r_max]

    ax0.imshow(im, aspect='auto', extent=extent, alpha=transparency, zorder=-1)

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    theta = np.linspace(0, 2 * np.pi, 100)
    r = 2 + np.sin(theta)
    ax1.plot(theta, r, color='blue', linewidth=2)

    file_name = r'C:\github\assetutilities\docs\leg_pycodes\add_image_to_ploar_plot.png'
    plt.savefig(file_name, dpi=800)
    plt.close()

image_path = r'C:\github\assetutilities\docs\leg_pycodes\add_image_to_plot.png'
r_min, r_max = 0,2.5
theta_min_deg, theta_max_deg = 150, 340
transparency = 0.3

add_image_to_polar_plot(image_path, r_min, r_max, theta_min_deg, theta_max_deg, transparency)
