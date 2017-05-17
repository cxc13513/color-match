
import numpy as np
import pdb
from scipy.spatial.distance import seuclidean
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_samples
from sklearn.metrics import silhouette_score


def calc_silhouette_score(arr1, arr2):
    '''Calculates sklearn's silhouette score + 1.

    INPUT: two numpy arrays
    OUTPUT: numpy.float64
    '''
    y_arr1 = np.zeros(shape=(len(arr1), 1))
    y_arr2 = np.ones(shape=(len(arr2), 1))
    y_comb = np.vstack((y_arr1, y_arr2))
    row = y_comb.shape[0]
    labels = y_comb.reshape(row, )
    X = np.vstack((arr1, arr2))
    # pdb.set_trace()
    score = silhouette_score(X, labels, metric='euclidean') + 1
    return score


def calc_silhouette_samples(arr1, arr2):
    '''Calculates sklearn's silhouette sample score + 1.

    INPUT: two numpy arrays
    OUTPUT: numpy.float64
    '''
    y_arr1 = np.zeros(shape=(len(arr1), 1))
    y_arr2 = np.ones(shape=(len(arr2), 1))
    y_comb = np.vstack((y_arr1, y_arr2))
    row = y_comb.shape[0]
    labels = y_comb.reshape(row, )
    X = np.vstack((arr1, arr2))
    score = silhouette_samples(X, labels, metric='euclidean') + 1
    return score


def calc_seuclidean(arr1, arr2):
    '''Calculates normalized dist when clusters only have one RGB point in each.

    INPUT: two numpy arrays
    OUTPUT: numpy.float64
    '''
    score = seuclidean(arr1, arr2)
    return score


def calc_distance(arr1, arr2):
    '''Calculates normalized dist when clusters only have one RGB point in each.

    INPUT: two numpy arrays, normalized for RGB space to between 0 and 2
            this matches the notation used for silhouette scores.
    OUTPUT: numpy.float64
    '''
    score = pairwise_distances((arr1/255*np.sqrt(2)), (arr2/255*np.sqrt(2)), metric='euclidean')
    return float(score)
