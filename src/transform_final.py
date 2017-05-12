# https://www.oreilly.com/learning/three-dimensional-plotting-in-matplotlib
# https://github.com/eriklindernoren/ML-From-Scratch/blob/master/unsupervised_learning/dbscan.py
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import pdb
from sklearn.cluster import DBSCAN

'''
The logic to return the center of the largest cluster (but be aware, the center itself may be meaningless with DBSCAN): sort the clusters by size, take the largest, calculate the centroid (using the logic provided in that blog post). Then you have a choice. You can either keep that calculated centroid as the "center point" or you can find the point in the cluster nearest to that centroid (as the author of that blog post seems to do).
http://stackoverflow.com/questions/33917999/using-dbscan-to-find-the-most-dense-cluster?rq=1
'''

'''
But in particular, DBSCAN does not compute the nearest core point.
So it does not have the information you are looking for!
You'll have to do it yourself.
Put all core points into a kdtree/balltree
Find the nearest neighbor using the index
Scikit-learn provides everything you need already,
it should be just a few lines.
'''


def create_final_X_dataset(db, df):
    # save down labels attribute, convert to pd series & add to df
    labels = db.labels_
    df['cluster_num'] = pd.Series(labels.tolist()).values
    # create mask for whether obvs is a core sample
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    # make 2 new smaller dfs with only obvs tied to non-noisy clusters
    X = np.array(df)
    subset = X[core_samples_mask]
    # covert back to df with smaller subset of observations & cluster label
    subset2 = subset.reshape((-1, 4))
    subset_df_w_clust = pd.DataFrame({'R': subset2[:, 0],
                                      'G': subset2[:, 1],
                                      'B': subset2[:, 2],
                                      'Clust': subset2[:, 3]})
    # create single combination RGB in order to find the most frequent
    subset_df_w_clust['combined'] = subset_df_w_clust.R.astype(str).str.cat(subset_df_w_clust.G.astype(str), sep='-').str.cat(subset_df_w_clust.B.astype(str), sep='-')
    # find most frequent RGB in each cluster
    subset_df_w_clust['count'] = subset_df_w_clust.groupby(['Clust', 'combined'])['combined'].transform('count')
    # extract most frequent R,G,B per cluster
    color_combo_arr = subset_df_w_clust[['R', 'G', 'B']].iloc[subset_df_w_clust.groupby(['Clust']).apply(lambda x: x['count'].idxmax())].as_matrix()
    '''
    FOR NOW, IGNORE ADDING WEIGHTS TO most frequent RGBs in each clust
    But I can add weights back in easily-> include 'count' when create matrix
    ALSO FOR LATER: USE MOST FREQUENT? OR DENSEST????
    dense still doesn't solve everything. would have to find densest,
    calc fake centroid, then find the nearest neighbor to that fake centroid,
    and use that as the representative from that cluster.
    '''
    # need to?? convert that np array to pandas df, with each element a column.

    pdb.set_trace()

    return color_combo_arr

    '''
    ASK!!
    color_combo_arr returns below array for each jpeg. shape: (2,3)
            array([[ 4,  4,  6],
               [27, 24, 21]])

    BUT that seems not ideal if I need to append alot of these together,
    and they could have varying lengths. Right? confirm if that's accurate.

    I think I need a df. but I've also read that it's really bad form
    to embed an array as an obvs in a pandas df. is that true? why?

    Or, could I do a nested array?

    Or, maybe turn into a set?

    GAHHHHHH

    Not sure what form to feed into classifiers.

    Also need to make sure classifiers all have jaccard distance params set.
    '''
