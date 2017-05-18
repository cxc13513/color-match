import cluster
import get_colorvalues
# import pdb
import save_scraped
import transform_final

# run in virtual env named clusterenv to get faster version of scikit-learn....
# source activate clusterenv
# http://stackoverflow.com/questions/16381577/scikit-learn-dbscan-memory-usage

'''The simple and most effective way to prevent Apple OSX to sleep:
    Terminal command:   $ pmset noidle
                        Preventing idle sleep (^C to exit)...
The only annoying thing maybe the user self has to end this manually
by issuing a 'Control-C'.
'''

# 1: get list of jpegs in folder
path = "/Users/colinbottles/Desktop/Cat/school/color-match/data/raw/"
jpg_list = save_scraped.get_files_in_folder(path)

# 1-small: use small list of jpegs for now
jpg_list_small = [
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/raw/1301.jpg',
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/raw/1302.jpg']

# 2: create empty list to hold final data.
X_clustered = []
X_baseline = []
list_jpgs_covered = []
# 3: loop over all functions for each jpg to get final data for each jpg
for index, jpg in enumerate(jpg_list):
    # 3a: converts jpg to np array
    pixel_values, rgb_or_not = get_colorvalues.convert_jpg_array(jpg,
                                                                 downsize_factor=0.5)
    # make sure the jpg is RGB, not b&w:
    if rgb_or_not == 'RGB':

        # 3b: plots raw pixel values
        # get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)

        # 3c: save down simple averaged pixel_values for baseline model
        X_baseline.append(get_colorvalues.get_baseline_arr(pixel_values))

        # 3d: clusters raw pixel values & keeps just the ones need
        csind, labels, raw_df = cluster.dbscan_indiv_pic(pixel_values,
                                                         epsilon=3,
                                                         min_clust_size=10,
                                                         algo='ball_tree',
                                                         dist_metric='euclidean',
                                                         num_jobs=2,
                                                         jpg_num=jpg)

        # 3e: plots clusters
        # cluster.plot_3dclusters(fitted_dbscan, raw_df, plot_dbscan=True)

        # 3f: transforms clustered pixel values into final format
        arr_one_color_combo = transform_final.create_final_X_dataset(csind,
                                                                     labels,
                                                                     raw_df)

        # 3g: appends arr_one_color_combo to final format
        X_clustered.append(arr_one_color_combo)

        # 3h: keeps tally of which jpgs were scrubbed in, in same oder as 3 f&g
        list_jpgs_covered.append(jpg)

    else:
        continue

# 4: pickle X_clustered & X_baseline
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
filename = 'pickled_list_arr'
basename = 'pickled_list_arr_baseline'
order = 'pickled_jpg_order'
pickled_clustered_path = transform_final.pick(X_clustered, filename, filepath)
pickled_baseline_path = transform_final.pick(X_baseline, basename, filepath)
pickled_order_path = transform_final.pick(list_jpgs_covered, order, filepath)
