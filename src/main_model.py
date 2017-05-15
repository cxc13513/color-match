import cluster
import get_colorvalues
# import model_pipeline
import numpy as np
import pandas as pd
import pdb
import silhouette
import transform_final

# 1: load pickled final_df
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
filename = 'pickled_list_arr'
basename = 'pickled_list_arr_baseline'
order = 'pickled_jpg_order'
pickled_clustered_path = filepath+filename
pickled_baseline_path = filepath+basename
pickled_order_path = filepath+order
list_clusters = transform_final.unpick(pickled_clustered_path)
list_baseline = transform_final.unpick(pickled_baseline_path)
list_order = transform_final.unpick(pickled_order_path)

# 2: load one 'new' photo
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/testing/'
name = 'bad4.jpg'
pic = filepath+name

# 3: get color values & cluster 'new' photo
pixel_values, rgb_or_not = get_colorvalues.convert_jpg_array(pic, downsize_factor=0.5)

# make sure the jpg is RGB, not b&w:
if rgb_or_not != 'L':

    # 3b: plots raw pixel values
    # get_colorvalues.plot_3dscatter_raw(pixel_values, plot_3dscatter=True)

    # 3c: save down simple averaged pixel_values for baseline model
    new_image_arr_base = get_colorvalues.get_baseline_arr(pixel_values)

    # 3d: clusters raw pixel values & keeps just the ones need
    fitted_dbscan, raw_df = cluster.dbscan_indiv_pic(pixel_values, epsilon=3,
                                                     min_clust_size=300,
                                                     algo='auto',
                                                     dist_metric='euclidean',
                                                     num_jobs=2, jpg_num=pic)

    # 3e: plots clusters
    # cluster.plot_3dclusters(fitted_dbscan, raw_df, plot_dbscan=True)

    # 3f: transforms clustered pixel values into final format
    new_image_arr_cl = transform_final.create_final_X_dataset(fitted_dbscan,
                                                              raw_df)

    # 4: calculate silhouette score in RGB space
    list_scores_cl = []
    for i in list_clusters:
        arr = list_clusters[i]
        score = silhouette.calc_silhouette_score(new_image_arr_cl, arr)
        list_scores_cl.append(score)

    # 5: calculate baseline score in RGB space
    list_scores_base = []
    for i in list_baseline:
        barr = list_baseline[i]
        if len(new_image_arr_base) == 1 & len(barr) == 1:
            baseline_score = silhouette.calc_distance(new_image_arr_base, barr)
            list_scores_base.append(baseline_score)
            '''have to figure out workaround for when both clusters are just points,
            then silhouette doesnt work obvs'''
        else:
            baseline_score = silhouette.calc_silhouette_score(new_image_arr_base, barr)
            list_scores_base.append(baseline_score)

    # 6: make df of silhouette & baseline scores & order
    len(list_scores_cl) == len(list_order)
    len(list_scores_base) == len(list_order)
    score_comparison = pd.DataFrame(np.column_stack([list_order, list_scores_base,
                                                    list_scores_cl]),
                                    columns=['jpg_path', 'baseline', 'clustered'])
    # zipped_clustered = zip(list_scores_base, list_order)
    # zipped_baseline = zip(list_baseline, list_order)
    # sorted(zipped_clustered, key=operator.itemgetter(1))
    # sorted(zipped_clustered)
    # sorted(zipped_baseline)
    # maybe_clustered = min([x for x,y in zipped_clustered])
    # maybe_baseline = min([x for x,y in zipped_baseline])

    # 8: find most similar image by referencing jpg_path
    min_baseline = score_comparison.min('baseline')
    min_clustered = score_comparison.min('clustered')

    # 5: instantiate pipeline object & then fit pipeline with X
    # unary_pipeline = model_pipeline.ModelPipeline(X, y)
    # f1, recall, precision = unary_pipeline.run_unary_classifiers()
    # 6: prob call in gridsearchcv to find params?
