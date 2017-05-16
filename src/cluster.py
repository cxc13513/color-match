from matplotlib import cm
import matplotlib.pyplot as plt
# from memory_profiler import profile
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
# import pdb
from sklearn.cluster import DBSCAN


def dbscan_indiv_pic(pixel_values, epsilon, min_clust_size,
                     algo, dist_metric, num_jobs, jpg_num):
    '''Cluster each picture's set of color values.

    INPUT:  np array
            DBSCAN parameters (eps, min_sample, algorithm, n_jobs)
    OUTPUT: list of arrays
            each array=set of unique RGB values in DBSCAN clusters per pic
            Currently, no weights for clusters.
    '''
    # convert data into pandas dataframe in order to feed into DBSCAN!!
    index = [str(i) for i in range(1, len(pixel_values)+1)]
    col_names = ['R', 'G', 'B']
    df = pd.DataFrame(pixel_values, index=index, columns=col_names)
    # fit DBSCAN for each picture:
    if len(df) < 2500:
        db = DBSCAN(eps=epsilon, min_samples=10, algorithm=algo,
                    metric=dist_metric)
    else:
        db = DBSCAN(eps=epsilon, min_samples=min_clust_size, algorithm=algo,
                    metric=dist_metric)
    db.fit(pixel_values)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    while n_clusters_ < 2:
        epsilon += 1
        if epsilon < 15:
            db = DBSCAN(eps=epsilon, min_samples=10, algorithm=algo,
                        metric=dist_metric)
            db.fit(pixel_values)
            n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
            print('JPG %s has %d clusters and %d epsilon' % (str(jpg_num),
                                                             n_clusters_,
                                                             epsilon))
        else:
            break
    else:
        print('JPG %s has %d clusters' % (str(jpg_num), n_clusters_))

    # also save down core sample indices to return
    core_sample_indices = db.core_sample_indices_
    return core_sample_indices, labels, df


def plot_3dclusters(db, df, plot_dbscan=False):
    '''optional plotting: - 3D scatter of DBSCAN-clusters vs. noise'''
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
