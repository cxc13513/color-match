# http://stackoverflow.com/questions/16381577/scikit-learn-dbscan-memory-usage
# http://stackoverflow.com/questions/39781262/find-the-location-that-occurs-most-in-every-cluster-in-dbscan?rq=1
# https://github.com/eriklindernoren/ML-From-Scratch/blob/master/unsupervised_learning/dbscan.py
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import pdb
import pickle
from PIL import Image
import scipy.spatial
from sklearn.cluster import DBSCAN

# https://www.quora.com/What-is-a-kd-tree-and-what-is-it-used-for
# http://groups.csail.mit.edu/graphics/classes/6.838/S98/meetings/m13/kd.html


def dbscan_indiv_pic(pixel_values, epsilon, min_clust_size,
                     algo, dist_metric, num_jobs):
    '''Cluster each picture's set of color values.

    INPUT:  np array
            DBSCAN parameters (eps, min_sample, algorithm, n_jobs)

    OUTPUT: list of arrays
            each array=set of unique RGB values in DBSCAN clusters per pic
            optional plotting: - 3D scatter of raw pixel values (R, G, B)
                               - 3D scatter of DBSCAN-clusters vs. noise
            Currently, no weights for clusters.
    '''
    # convert data into pandas dataframe in order to feed into DBSCAN!!
    index = [str(i) for i in range(1, len(pixel_values)+1)]
    col_names = ['R', 'G', 'B']
    df = pd.DataFrame(pixel_values, index=index, columns=col_names)
    # fit DBSCAN for each picture:
    db = DBSCAN(eps=epsilon, min_samples=min_clust_size,
                algorithm=algo, metric=dist_metric, n_jobs=num_jobs)
    db.fit(df)
    # print how many clusters are in this pic, ignoring noise if present.
    n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    return db, df


def plot_3dclusters(db, df, plot_dbscan=False):
    if plot_dbscan is True:
        # finds unique clusters & adds to df
        labels = db.labels_
        df['cluster_num'] = pd.Series(labels.tolist()).values
        unique_labels = set(labels)
        # create mask for whether obvs is a core sample
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        # convert df to np array
        X = np.array(df)
        # Assigns diff colors to each unique cluster & uses black for noise
        cm_subsection = np.linspace(0.0, 1.0, len(unique_labels))
        colors = [cm.jet(x) for x in cm_subsection]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for k, color in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                color = 'k'
            class_member_mask = (labels == k)
            xy = X[class_member_mask & core_samples_mask]
            ax.scatter3D(xy[:, 0], xy[:, 1], xy[:, 2], c=xy[:, 2],
                         s=10, alpha=0.5)
            zy = X[class_member_mask & ~ core_samples_mask]
            ax.scatter3D(zy[:, 0], zy[:, 1], zy[:, 2], c=color,
                         s=0.05, alpha=0.001)
        # Set viewpoint/title
        ax.azim = -160
        ax.elev = 30
        plt.title('Estimated number of clusters: %d' % (len(unique_labels)-1))
        plt.show()


def other_dbscan(points, eps, min_pts):
    # convert data into pandas dataframe in order to feed into DBSCAN!!
    index = [str(i) for i in range(1, len(points)+1)]
    col_names = ['R', 'G', 'B']
    df = pd.DataFrame(points, index=index, columns=col_names)

    tree = scipy.spatial.cKDTree(points)
    neighbors = tree.query_ball_point(points, eps)
    # list of (set, set)'s, to distinguish core/reachable points
    clusters = []
    visited = set()
    for i in range(len(points)):
        if i in visited:
            continue
        visited.add(i)
        if len(neighbors[i]) >= min_pts:
            clusters.append(({i}, set()))  # core
            to_merge_in_cluster = set(neighbors[i])
            while to_merge_in_cluster:
                j = to_merge_in_cluster.pop()
                if j not in visited:
                    visited.add(j)
                    if len(neighbors[j]) >= min_pts:
                        to_merge_in_cluster |= set(neighbors[j])
                if not any([j in c[0] | c[1] for c in clusters]):
                    if len(neighbors[j]) >= min_pts:
                        clusters[-1][0].add(j)  # core
                    else:
                        clusters[-1][1].add(j)  # reachable
    return clusters, df
