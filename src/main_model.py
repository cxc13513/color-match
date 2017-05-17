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

# set which photo in testing want to score for
test_photo_number = 1

# 4: calculate silhouette score in RGB space
print(test_order[test_photo_number])
list_scores_cl = []
new_image_arr_cl = test_clusters[test_photo_number]

for arr in list_clusters:
    score = silhouette.calc_silhouette_score(arr, new_image_arr_cl)
    list_scores_cl.append(score)

# 5: calculate baseline score in RGB space
list_scores_base = []
new_image_barr_cl = test_baseline[test_photo_number]
for barr in list_baseline:
    if len(new_image_barr_cl) == 1 & len(barr) == 1:
        '''workaround for when both clusters are just points,
           then silhouette doesnt work obvs'''
        baseline_score = silhouette.calc_distance(barr, new_image_barr_cl)
        list_scores_base.append(baseline_score)
    else:
        baseline_score = silhouette.calc_silhouette_score(barr,
                                                          new_image_barr_cl)
        list_scores_base.append(baseline_score)

# 6: make df of silhouette & baseline scores & order
score_comparison = pd.DataFrame(np.column_stack([list_order, list_scores_base,
                                                list_scores_cl]),
                                columns=['jpg_path', 'baseline', 'clustered'])

# 7: clean df: convert column format, round if numeric, parse if string
score_comparison = score_comparison.astype(dtype={"jpg_path": "str",
                                                  "baseline": "float64",
                                                  "clustered": "float64"})

score_comparison[['baseline', 'clustered']] = score_comparison[['baseline', 'clustered']].apply(lambda x: pd.Series.round(x, 2))
score_comparison['jpg'] = score_comparison['jpg_path'].apply(lambda x: x.split('/')[-1])
score_comparison = score_comparison.drop('jpg_path', axis=1)

# 8: find top couple most similar (e.g., 5 lowest scores)
print(' ')
print('most similar according to clustered')
print(score_comparison.sort_values(['clustered'], ascending=True).head(10))
print(' ')
print('most similar according to baseline')
print(score_comparison.sort_values(['baseline'], ascending=True).head(10))
