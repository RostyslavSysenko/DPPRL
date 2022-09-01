from sklearn.neighbors import NearestNeighbors
import numpy as np


def linkDynamically(encodingString, clusterListObject):

    clusterListObject.initialClusterRepresentationCompile()
    
    knn = NearestNeighbors(n_neighbors=1)
    knn.fit(clusterListObject.clusterRepresentations)
    encodingArr = [int(char) for char in encodingString]
    distance_mat, neighbours_mat = knn.kneighbors(encodingArr)