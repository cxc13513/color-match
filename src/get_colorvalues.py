# import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import pdb
from PIL import Image


def convert_jpg_array(jpg, downsize_factor=0.5):
    '''Cluster each picture's set of color values.

    INPUT:  list of file names (string)
            downsize factor (how much to compress from original size)
            DBSCAN parameters (eps, min_sample, algorithm, n_jobs)
    OUTPUT: np array with all raw pixel RGB values for one picture
    '''
    pict = Image.open(jpg, 'r')
    rgb_or_not = pict.mode
    original_width, original_height = pict.size
    if original_width < 400:
        pict = pict
    else:
        pict = pict.resize((int(original_width*downsize_factor),
                            int(original_height*downsize_factor)))
    new_width, new_height = pict.size
    pixel_values = np.array(pict.getdata())
    return pixel_values, rgb_or_not


def get_baseline_arr(pixel_values):
    '''Calcs average R, G, B across one image as baseline.'''
    mean_R = np.mean(pixel_values[:, 0])
    mean_G = np.mean(pixel_values[:, 1])
    mean_B = np.mean(pixel_values[:, 2])
    baseline_arr = np.array([[mean_R, mean_G, mean_B]])
    return baseline_arr


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)


def convert_to_hex(arr):
    """Return list of colors as #rrggbb for the given color values."""
    list_hex = []
    for i in range(len(arr)):
        red = int(np.array(arr[i]).tolist()[0])
        green = int(np.array(arr[i]).tolist()[1])
        blue = int(np.array(arr[i]).tolist()[2])
        list_hex.append(str.upper('#%02x%02x%02x' % (red, green, blue)))
    return list_hex


def plot_3dscatter_raw(pixel_values, plot_3dscatter=False):
    '''optional plotting: - 3D scatter of raw pixel values (R, G, B)'''
    if plot_3dscatter is True:
        # initialize empty arrays r, g, and b
        r = np.array([])
        g = np.array([])
        b = np.array([])
        for i in range(len(pixel_values)):
            r = np.r_[r, pixel_values[i][0]]
            g = np.r_[g, pixel_values[i][1]]
            b = np.r_[b, pixel_values[i][2]]
        # plot 3d scatter of pixel_values
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter3D(r, g, b, c=b, s=0.1, alpha=0.1)
        # Set viewpoint/title
        ax.azim = -160
        ax.elev = 30
        plt.show()
