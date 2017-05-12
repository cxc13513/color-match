# https://www.oreilly.com/learning/three-dimensional-plotting-in-matplotlib
# https://github.com/eriklindernoren/ML-From-Scratch/blob/master/unsupervised_learning/dbscan.py
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pdb
from PIL import Image


def convert_jpg_array(jpg, downsize_factor=0.5):
    '''Cluster each picture's set of color values.

    INPUT:  list of file names (string)
            downsize factor (how much to compress from original size)
            DBSCAN parameters (eps, min_sample, algorithm, n_jobs)
    OUTPUT: np array with all raw pixel RGB values for one picture
    optional plotting: - 3D scatter of raw pixel values (R, G, B)
    '''
    pict = Image.open(jpg, 'r')
    original_width, original_height = pict.size
    # downsize pict with an ANTIALIAS filter (gives the highest quality)
    downsize_factor = downsize_factor
    pict = pict.resize((int(original_width*downsize_factor),
                       int(original_height*downsize_factor)),
                       Image.ANTIALIAS)
    new_width, new_height = pict.size
    pixel_values = np.array(pict.getdata())
    return pixel_values, original_height, original_width


def plot_3dscatter_raw(pixel_values, plot_3dscatter=False):
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
        '''
        MAYBE TRY HISTOGRAM INSTEAD?
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter3D(r, g, b, c=b, s=0.01, alpha=0.01)
        # Set viewpoint/title
        ax.azim = -160
        ax.elev = 30
        plt.show()
