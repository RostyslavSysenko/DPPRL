from sklearn.metrics import pairwise_distances
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree
from scipy.spatial.distance import pdist 
from sklearn.cluster import AgglomerativeClustering


# input parameter: 2d array of encoded strings 



# split and convert to array (no delimiter)

    # pass string through list function 
list(string)


# apply heirarchical clustering 
distances = pdist(df, 'euclidean')
    # Pairwise distances between observations in n-dimensional space.
    # Computes the distance between m points using Euclidean distance (2-norm) as the distance metric between the points. 
    # The points are arranged as m n-dimensional row vectors in the matrix X.
distances.shape
linkage_matrix = linkage(distances, method = 'centroid' )

#plt.figure(figsize = (32,18))
#dendrogram(linkage_matrix, labels = df.index, orientation = 'left')
#plt.show

# conduct bottom up clustering based on number of clusters derived from dendrogram
# algorithm determines number of clusters 
# compute_full_tree = True --> does not stop construction of tree at n_clusters 
# distance threshold --> linkage distance threshold above which, clusters will not be merged
cluster = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='ward', compute_full_tree=True, distance_threshold=200)

# returns an array 
cluster_array = cluster.fit_predict()

#convert to list 
cluster_list = cluster_array.tolist()

# output list of clusters 
