import model_pipeline
import pdb
import silhouette
import transform_final

# 1: load pickled final_df
filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
filename = 'pickled_list_arr'
basename = 'pickled_list_arr_baseline'
pickled_clustered_path = filepath+filename
pickled_baseline_path = filepath+basename
list_clusters = transform_final.unpick(pickled_clustered_path)
list_baseline = transform_final.unpick(pickled_baseline_path)

# 2: calculate silhouette & baseline score in RGB space
new_image = list_clusters[0]
arr2 = list_clusters[1]
score = silhouette.calc_silhouette_score(new_image, arr2)
# barr1 = list_baseline[0]
barr2 = list_baseline[1]
if len(new_image) == 1 & len(barr2) == 1:
    baseline_score = silhouette.calc_distance(new_image, barr2)
    '''have to figure out workaround for when both clusters are just points,
    then silhouette doesnt work obvs'''
else:
    baseline_score = silhouette.calc_silhouette_score(new_image, barr2)

# 3: instantiate pipeline object & then fit pipeline with X
unary_pipeline = model_pipeline.ModelPipeline(X, y)
f1, recall, precision = unary_pipeline.run_unary_classifiers()

# 4: prob call in gridsearchcv to find params?
