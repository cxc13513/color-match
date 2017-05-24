import cluster
import get_colorvalues
import pdb

# run in virtual env named clusterenv to get faster version of scikit-learn....
# source activate clusterenv
# http://stackoverflow.com/questions/16381577/scikit-learn-dbscan-memory-usage

'''The simple and most effective way to prevent Apple OSX to sleep:
    Terminal command:   $ pmset noidle
                        Preventing idle sleep (^C to exit)...
The only annoying thing maybe the user self has to end this manually
by issuing a 'Control-C'.
'''

# # 1: get list of jpegs in folder
# path = "/Users/colinbottles/Desktop/Cat/school/color-match/data/addtomaindata/"
# jpg_testing = save_scraped.get_files_in_folder(path)

# 1-testing: crunch thru testing sample of jpegs here to see if run faster
jpg_small_testing = [
    '/Users/colinbottles/Desktop/Cat/school/color-match/data/addtomaindata/toadd15.jpg']

# 2: create empty list to hold final data.
X_clustered = []
X_baseline = []
list_jpgs_covered = []

# 3: loop over all functions for each jpg to get final data for each jpg
for index, jpg in enumerate(jpg_small_testing):
    # 3a: converts jpg to np array
    pixel_values, rgb_or_not = get_colorvalues.convert_jpg_array(jpg,
                                                                 downsize_factor=0.5)

    # 3b: plots raw pixel values
    # get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)
    get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)

    # # 3c: save down simple averaged pixel_values for baseline model
    # X_baseline.append(get_colorvalues.get_baseline_arr(pixel_values))
    # #
    # # 3d: clusters raw pixel values & keeps just the ones need
    # csind, labels, raw_df = cluster.dbscan_indiv_pic(pixel_values,
    #                                                  epsilon=3,
    #                                                  min_clust_size=300,
    #                                                  algo='ball_tree',
    #                                                  dist_metric='euclidean',
    #                                                  num_jobs=2,
    #                                                  jpg_num=jpg)
    #
    # # 3e: plots clusters
    # cluster.plot_3dclusters(fitted_dbscan, raw_df, plot_dbscan=True)
