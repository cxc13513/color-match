import cluster
import get_colorvalues
import numpy as np
import pandas as pd
import pdb
import save_scraped
import silhouette
import transform_final
from matplotlib import cm
import matplotlib.pyplot as plt
# from memory_profiler import profile
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D


def analyzer(path):
    # 1: convert uploaded picture from web app
    # 1a: get list of jpegs in upload folder
    # path = "/Users/colinbottles/Desktop/Cat/school/color-match/uploads/"
    jpg_uploaded = save_scraped.get_files_in_folder(path)

    try:
        jpg_uploaded.remove('/Users/colinbottles/Desktop/Cat/school/color-match/uploads/.DS_Store')
    except ValueError:
        pass
    else:
        pass

    # pdb.set_trace()

    # 2: create empty list to hold final data.
    U_clustered = []
    U_baseline = []
    U_jpgs_covered = []
    # 1b: loop over all functions for each jpg to get final data for each jpg
    for item in jpg_uploaded:
        # 3a: converts jpg to np array
        pixel_values, rgb_or_not = get_colorvalues.convert_jpg_array(item,
                                                                     downsize_factor=0.25)
        # make sure the jpg is RGB, not b&w:
        if rgb_or_not == 'RGB':

            # 3b: plots raw pixel values
            # get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)

            # save down simple averaged pixel_values for baseline model
            U_baseline.append(get_colorvalues.get_baseline_arr(pixel_values))

            # pdb.set_trace()

            # clusters raw pixel values & keeps just the ones need
            csind, labels, raw_df = cluster.dbscan_indiv_pic(pixel_values,
                                                             epsilon=3,
                                                             min_clust_size=10,
                                                             algo='ball_tree',
                                                             dist_metric='euclidean',
                                                             num_jobs=2,
                                                             jpg_num=item)

            # transforms clustered pixel values into final format
            arr_one_color_combo = transform_final.create_final_X_dataset(csind,
                                                                         labels,
                                                                         raw_df)
            # appends arr_one_color_combo to final format
            U_clustered.append(arr_one_color_combo)
            # keeps tally of which jpgs were scrubbed in, in same oder as 3 f&g
            U_jpgs_covered.append(item)

    # 2: unpickle clustered/baseline arrays & order for calculations
    filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
    filename = 'pickled_list_arr'
    basename = 'pickled_list_arr_baseline'
    order = 'pickled_jpg_order'
    list_clusters = transform_final.unpick(filepath+filename)
    list_baseline = transform_final.unpick(filepath+basename)
    list_order = transform_final.unpick(filepath+order)

    # 3: set which photo in uploaded want to score for (order)
    uploaded = 0

    # 4: calculate silhouette score in RGB space & convert all RGB to HEX for web
    list_scores_cl = []
    list_hex_arr = []

    uploaded_arr = U_clustered[uploaded]
    list_hex_uploaded_arr = get_colorvalues.convert_to_hex(uploaded_arr)

    for arr in list_clusters:
        score = silhouette.calc_silhouette_score(arr, uploaded_arr)
        list_scores_cl.append(score)
        hex_arr = get_colorvalues.convert_to_hex(arr)
        list_hex_arr.append(hex_arr)

    # 5: calculate baseline score in RGB space & convert all RGB to HEX for web
    list_scores_base = []
    list_hex_barr = []

    uploaded_barr = U_baseline[uploaded]
    list_hex_uploaded_barr = get_colorvalues.convert_to_hex(uploaded_barr)

    for barr in list_baseline:
        if len(uploaded_barr) == 1 & len(barr) == 1:
            '''workaround for when both clusters are just points,
               then silhouette doesnt work obvs'''
            baseline_score = silhouette.calc_distance(barr, uploaded_barr)
            list_scores_base.append(baseline_score)
        else:
            baseline_score = silhouette.calc_silhouette_score(barr,
                                                              uploaded_barr)
            list_scores_base.append(baseline_score)
        hex_barr = get_colorvalues.convert_to_hex(barr)
        list_hex_barr.append(hex_barr)

    # 6: make df of silhouette & baseline scores & order
    score_comparison = pd.DataFrame(np.column_stack([list_order, list_scores_base,
                                                    list_scores_cl, list_hex_arr,
                                                    list_hex_barr]),
                                    columns=['jpg_path', 'baseline', 'clustered',
                                             'hex_clustered', 'hex_baseline'])

    # 7: clean df: convert column format, round if numeric, parse if string
    score_comparison = score_comparison.astype(dtype={"jpg_path": "str",
                                                      "baseline": "float64",
                                                      "clustered": "float64",
                                                      "hex_clustered": "str",
                                                      "hex_baseline": "str"})

    score_comparison[['baseline', 'clustered']] = score_comparison[['baseline', 'clustered']].apply(lambda x: pd.Series.round(x, 2))
    score_comparison['jpg'] = score_comparison['jpg_path'].apply(lambda x: x.split('/')[-1])
    score_comparison = score_comparison.drop('jpg_path', axis=1)

    '''NOW I HAVE TO FIGURE OUT WHAT TO RETURN TO SHOW ON WEBAPP'''

    # 8: pred if color combination is appealing (e.g., 5 lowest scores)
    print(' ')
    print('most similar according to clustered')
    print(score_comparison.sort_values(['clustered'], ascending=True).head(10))
    print(' ')
    print('most similar according to baseline')
    print(score_comparison.sort_values(['baseline'], ascending=True).head(10))

    # # 8: pred if color combination is appealing (e.g., 5 lowest scores)
    # range_scores = range(96, 105, 1)
    # print(' ')
    # print('most similar according to clustered')
    # print(score_comparison[(score_comparison['clustered']*100) in range_scores])
    # print(' ')
    # print('most similar according to baseline')
    # print(score_comparison[score_comparison['baseline' == 1.00]].sort_values(['jpg'], ascending=True).head(5))

    # 9: RETURN!!
    return('this sort of works!')

    ''' TRY RUNNING WEB APP AGAIN NOW THAT THIS CODE IS FIXED TO RETURN OK !!!!!'''
