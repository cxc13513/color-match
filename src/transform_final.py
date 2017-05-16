import numpy as np
import pandas as pd
import pickle


def pick(dataset, filename, filepath):
    '''Pickle file and save down'''
    pickled_name_path = filepath+filename
    with open(pickled_name_path, 'wb') as f:
        pickle.dump(dataset, f)
    return pickled_name_path


def unpick(pickled_name_path):
    '''Unpickle file and load'''
    with open(pickled_name_path, 'rb') as f:
        final_df = pickle.load(f)
    return final_df


def create_final_X_dataset(csind, labels, df):
    '''Extracts most frequent RGB values from each cluster.

    INPUT: pandas dataframe, fitted dbscan
    OUTPUT: numpy array
    '''
    # save down labels attribute, convert to pd series & add to df
    df['cluster_num'] = pd.Series(labels.tolist()).values
    # create mask for whether obvs is a core sample
    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[csind] = True
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

    # delete manually all unnecessary dfs
    to_delete = [df, X, subset2, subset_df_w_clust]
    del to_delete

    # return the only big thing left
    return color_combo_arr
