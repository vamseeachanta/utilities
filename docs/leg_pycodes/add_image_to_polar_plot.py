import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def add_image_to_polar_plot(image_path, r_min, r_max, theta_min_deg, theta_max_deg, alpha):
    """
    Add an image to a polar plot with specified parameters.

    """
    theta_min = np.deg2rad(theta_min_deg)
    theta_max = np.deg2rad(theta_max_deg)

    im = Image.open(image_path)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    extent = [theta_min, theta_max, r_min, r_max]

    ax.imshow(im, aspect='auto', extent=extent, alpha=transparency, zorder=-1)

    theta = np.linspace(0, 2 * np.pi, 100)
    r = 2 + np.sin(theta)
    ax.plot(theta, r, color='blue', linewidth=2)

    plt.show()

image_path = r'C:\github\assetutilities\docs\leg_pycodes\add_image_to_plot.png'
r_min, r_max = 0,2.5
theta_min_deg, theta_max_deg = 155, 338
transparency = 0.3

add_image_to_polar_plot(image_path, r_min, r_max, theta_min_deg, theta_max_deg, transparency)
