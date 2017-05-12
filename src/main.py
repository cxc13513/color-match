# GOOD DISCUSSION OF ONE CLASS SVMs: http://rvlasveld.github.io/blog/2013/07/12/introduction-to-one-class-support-vector-machines/
# ISOLATION FOREST:
# http://stackoverflow.com/questions/43063031/how-to-use-isolation-forest
# https://perso.telecom-paristech.fr/~goix/nicolas_goix_osi_presentation.pdf
#
import cluster
import get_colorvalues
import model_pipeline
import numpy as np
import pdb
import pickle
import save_scraped
import transform_final


def pickle_finaldf(dataset, filename, filepath):
    pickled_name_path = filepath+filename
    with open(pickled_name_path, 'wb') as f:
        pickle.dump(dataset, f)
    return pickled_name_path


def unpickle_finaldf(pickled_name_path):
    with open(pickled_name_path, 'rb') as f:
        final_df = pickle.load(f)
    return final_df

# 1: get list of jpegs in folder
path = "/Users/colinbottles/Desktop/Cat/school/color-match/data/"
jpg_list = save_scraped.get_files_in_folder(path)

# 2: use small list of jpegs for now
jpg_list_small = [
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/10.jpg',
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/11.jpg',
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/12.jpg',
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/13.jpg']

# 3: loop over all functions for each jpg to get final data for each jpg
for jpg in jpg_list_small:
    # 3a: converts jpg to np array
    pixel_values, h, w = get_colorvalues.convert_jpg_array(jpg, downsize_factor=0.5)
    # 3b: plots raw pixel values
    # get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)

    # 3c: clusters raw pixel values & keeps just the ones need
    '''
    need to find some rule to adjust epsilon and min_clust_size
    for different sized jpgs (e.g., 1600x1200 vs 100x75)
    '''
    fitted_dbscan, raw_df = cluster.dbscan_indiv_pic(pixel_values, epsilon=3,
                                                     min_clust_size=600,
                                                     algo='auto',
                                                     dist_metric='euclidean',
                                                     num_jobs=1)
    # try another dbscan with kdtree and see if it's faster/better....
    # clusters, df = cluster.other_dbscan(pixel_values, eps=3, min_pts=900)

    # 3d: plots clusters
    # cluster.plot_3dclusters(fitted_dbscan, raw_df, plot_dbscan=True)
    # 3e: transforms pixel values into an array...not sure final format?
    arr_one_color_combo = transform_final.create_final_X_dataset(fitted_dbscan,
                                                                 raw_df)
    # 3f: appends df_one_row to final_df
    # check to see if you can append dfs with different number of rows?

    pdb.set_trace()

# 4: pickle final_df
filename = 'pickled_final_df'
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/'
pickled_name_path = pickle_finaldf(final_df, filename, filepath)

# 5: load pickled final_df
X = unpickle_finaldf(pickled_name_path)

# 6: create labels
y = np.ones((len(X), 1))

# 7: instantiate pipeline object & then fit pipeline with X
unary_pipeline = model_pipeline.ModelPipeline(X, y)
f1, recall, precision = unary_pipeline.run_unary_classifiers()

# 8: prob call in gridsearchcv to find params?
