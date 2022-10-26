from sklearn.neighbors import NearestNeighbors
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *


class DynamicClusterer:
    def findBestClusterForRow(self, blockingTurnedOn, row, operation, indexer, clusterAggregations):
        """
        - the idea of taking 2 best clusters is so we can somewhat judge uncertainty of clustering
        by checking how close the 2nd cluster comes to the first
        """
        
        knn_classifier = NearestNeighbors(n_neighbors=2, metric="cosine")

        if (not blockingTurnedOn):
            knn_classifier.fit(clusterAggregations) # fit the model based on the whole data
            distance_mat, neighbours_vec = knn_classifier.kneighbors([row.rowListRepresentation])
            
            clusterIdxBest1= neighbours_vec[0][0] # gets us index of cluster that we want to modify
            clusterIdxInClusterListBest1 = clusterIdxBest1

        else: # else if indexing is enabled
            #check to make sure that indexing is done
            assert not indexer.indexingHasNotBeenDoneYet(), "indexing not done"
            indexedClusterList = indexer.getClustersWithAtLeast1RowWithSameKey(row)
            formattedClusterAggregations = self.listOfClustersTo2DArrayOfClustAggr(indexedClusterList)
            
            knn_classifier.fit(formattedClusterAggregations) #fit the model based on subset of data
            distance_mat, neighbours_vec = knn_classifier.kneighbors([row.rowListRepresentation])
        
            clusterIdxBest1 = neighbours_vec[0][0] # gets us index of cluster that we want to modify
            clusterIdxInClusterListBest1 =  indexedClusterList[clusterIdxBest1].getId()



        cosSimBst1 = 1 - distance_mat[0][0]
        cosSimBst2 = 1 - distance_mat[0][1]

        certaintyScore = None
        
        if operation == Operation.INSERT:
            certaintyScore = DynamicClusterer.getInsertionCertainty(cosSimBst1,cosSimBst2)
        else: # most be considering delete or modification
            certaintyScore = cosSimBst1 # the certainty for modification and delete is just the similarity for best match

        #print("cos sim: "+str(cosineSimilarity) + " & reccomended neighbout is at idx: " + str(clusterIdx))
        return clusterIdxInClusterListBest1,certaintyScore

    
    def getInsertionCertainty(cosSimBst1,cosSimBst2):
        # returns certainty that row belong to particular cluster for the purpose of insertion 
        # 
        # behaviour this certainty score exhibits: 
        # - certainty is in [0,1]
        # - when simDiff (difference in similarity scores between best 2 matches) is low (close to 0), certainty is lower since we are torn between 2 best picks
        # - when cosSimBst1 is high (close to 1) certainty should be high since we found good matching cluster

        if (cosSimBst1>cosSimBst2 and cosSimBst1>0):
            diffScore = abs(cosSimBst1-cosSimBst2)/2
            certainty = (cosSimBst1*diffScore+1)/2 #mapping it onto [0,1]
        else:
            certainty = 0

        return certainty

    def listOfClustersTo2DArrayOfClustAggr(clusterList):
        clusterListRepr2D = list()

        for cluster in clusterList:
            clusterListRepr2D.append(cluster.getClusterListRepresentation())
            
        return clusterListRepr2D
