import numpy as np
import pandas as pd
import pdb
import silhouette
import transform_final

# 1: load pickled clustered/baseline arrays & order
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
filename = 'pickled_list_arr'
basename = 'pickled_list_arr_baseline'
order = 'pickled_jpg_order'
list_clusters = transform_final.unpick(filepath+filename)
list_baseline = transform_final.unpick(filepath+basename)
list_order = transform_final.unpick(filepath+order)

# 1: load TESTING pickled clustered/baseline arrays & order
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
filename = 'pickled_testing_arr'
basename = 'pickled_testing_arr_baseline'
order = 'pickled_testing_order'
test_clusters = transform_final.unpick(filepath+filename)
test_baseline = transform_final.unpick(filepath+basename)
test_order = transform_final.unpick(filepath+order)

# 4: calculate silhouette score in RGB space
list_scores_cl = []
new_image_arr_cl = test_clusters[0]
for arr in list_clusters:
    score = silhouette.calc_silhouette_score(new_image_arr_cl, arr)
    list_scores_cl.append(score)

# 5: calculate baseline score in RGB space
list_scores_base = []
new_image_arr_cl = test_clusters[0]
for barr in list_baseline:
    if len(new_image_arr_cl) == 1 & len(barr) == 1:
        baseline_score = silhouette.calc_distance(new_image_arr_cl, barr)
        list_scores_base.append(baseline_score)
        '''have to figure out workaround for when both clusters are just points,
        then silhouette doesnt work obvs'''
    else:
        baseline_score = silhouette.calc_silhouette_score(new_image_arr_cl, barr)
        list_scores_base.append(baseline_score)

# 6: make df of silhouette & baseline scores & order
len(list_scores_cl) == len(list_order)
len(list_scores_base) == len(list_order)

score_comparison = pd.DataFrame(np.column_stack([list_order, list_scores_base,
                                                list_scores_cl]),
                                columns=['jpg_path', 'baseline', 'clustered'])

print(score_comparison.head())

# 7: find most similar image by referencing jpg_path
print(score_comparison.iloc[score_comparison['baseline'].idxmin()])
print(score_comparison.iloc[score_comparison['clustered'].idxmin()])

# 8: if
