
# LATER: convert color mapping from RGB to hue, saturation, and brightness levels
# LATER: calculate silhouette score using just the hue values
# REALLY AWESOME RESOURCE http://stackoverflow.com/questions/9018016/how-to-compare-two-colors-for-similarity-difference


'''
FOR NOW, IGNORE ADDING WEIGHTS TO most frequent RGBs in each clust
But I can add weights back in easily-> include 'count' when create matrix
ALSO FOR LATER: USE MOST FREQUENT? OR DENSEST????
dense still doesn't solve everything. would have to find densest,
calc fake centroid, then find the nearest neighbor to that fake centroid,
and use that as the representative from that cluster.
'''
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


# http://stackoverflow.com/questions/16381577/scikit-learn-dbscan-memory-usage
# http://stackoverflow.com/questions/39781262/find-the-location-that-occurs-most-in-every-cluster-in-dbscan?rq=1
# https://github.com/eriklindernoren/ML-From-Scratch/blob/master/unsupervised_learning/dbscan.py
# https://www.quora.com/What-is-a-kd-tree-and-what-is-it-used-for
# http://groups.csail.mit.edu/graphics/classes/6.838/S98/meetings/m13/kd.html
