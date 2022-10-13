from array import *
from sklearn.neighbors import NearestNeighbors

from enum import Enum

class Indexer:
    def __init__(self,indexingBitStart=None, indexingBitEnd = None):
        self.indexingDictionary = dict() # used for indexing
        self.indexingBitStart = indexingBitStart
        self.indexingBitEnd = indexingBitEnd
    
    def indexingHasNotBeenDoneYet(self):
        return len(self.indexingDictionary) == 0

    def initialIndexBuild(self):
        # TO-DO
        # build the indexing into the self.indexingDictionary
        pass
    
    def getIndexingKey(self,row):
        # TO-DO
        # takes in a row and based on the indexing specification of ClusterList extracts the indexing key and returns it
        pass

    def updateIndexingDict():
        # when row is inserted with indexing turned on, the index should update after insertion
        pass

class DynamicClusterer:
    def findBestClusterForRow(blockingTurnedOn,row,operation, indexer,clusterAggregations):
        """
        - the idea of taking 2 best clusters is so we can somewhat judge uncertainty of clustering
        by checking how close the 2nd cluster comes to the first
        """
        if(blockingTurnedOn):
            if(indexer.indexingHasNotBeenDoneYet()):
                indexer.initialIndexBuild()
            indexingKey = indexer.getIndexingKey()
        
        knn_classifier = NearestNeighbors(n_neighbors=2, metric="cosine")

        if (not blockingTurnedOn):
            knn_classifier.fit(clusterAggregations) # fit the model based on the whole data
        else: # else if indexing is enabled
            assert indexer.indexingHasNotBeenDoneYet(), "indexing not done"
            indexedClusterAggregations = indexer.indexingDictionary[indexingKey]
            knn_classifier.fit(indexedClusterAggregations) #fit the model based on subset of data

        distance_mat, neighbours_vec = knn_classifier.kneighbors([row.rowListRepresentation])
        
        clusterIdxBest1= neighbours_vec[0][0] # gets us index of cluster that we want to modify
        
        cosSimBst1 = 1 - distance_mat[0][0]
        cosSimBst2 = 1 - distance_mat[0][1]

        certaintyScore = None
        
        if operation == Operation.INSERT:
            certaintyScore = ClusterList.getInsertionCertainty(cosSimBst1,cosSimBst2)
        else: # most be considering delete or modification
            certaintyScore = cosSimBst1 # the certainty for modification and delete is just the similarity for best match

        #print("cos sim: "+str(cosineSimilarity) + " & reccomended neighbout is at idx: " + str(clusterIdx))
        return clusterIdxBest1,certaintyScore

    
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


class ClusterList:
    def __init__(self, certaintyThreshold = 0.9,clusterAggrFunction = AggrFunct.mean,indexingBitStart=None, indexingBitEnd = None ):
        self.nextAvailIndex = 0
        self.certaintyThreshold = certaintyThreshold
        self.clusterAggrFunction =clusterAggrFunction
        self.clusterList = []
        self.clusterAggregations = []; # 2d array of clusters and each cluster array contains 0/1 bit encodings

        self.indexer = Indexer(indexingBitStart, indexingBitEnd)

    def __addNewClusterToClusterList(self,clusterObj):
        # insertion
        clusterObj.updateClusterOnClusterListInsertion(self,self.nextAvailIndex)
        self.nextAvailIndex = self.nextAvailIndex+1
        self.clusterAggregations.append(clusterObj.getClusterListRepresentation())
        self.clusterList.append(clusterObj)

    def __growExistingClusterInAClusterList(self,row, clusterIdxToWhichWeAdd):
        self.clusterList[clusterIdxToWhichWeAdd].addOneRowToCluster(row) #CLUSTER gets updated
        self.clusterAggregations[clusterIdxToWhichWeAdd] = self.clusterList[clusterIdxToWhichWeAdd].getClusterListRepresentation()

    def addClusterStaticly(self,clusterObj):
        # assign and increment index
        self.__addNewClusterToClusterList(clusterObj)


    def updateRowDynamically(self, idx, dbIdx, row,  blockingTurnedOn=False):
        pass


    def deleteRowDynamically(self, idx, dbIdx, row,  blockingTurnedOn=False):
        pass

    
    def addRowDynamic(self, row, blockingTurnedOn=False):
        # this is an implimentation of dynamic linkage which refits the model every time a dynamic linkage is needed and then finds 1 NN based on that newly created model
        # we assume the order of clusers never changes (meaning clusters are never deleted or reordered)
        
        clusterIdx,selectionCertainty = DynamicClusterer.findBestClusterForRow(blockingTurnedOn,row,Operation.INSERT, self.indexer,self.clusterAggregations)

        # here we conduct the insertion operation
        if (selectionCertainty>self.certaintyThreshold): # we decide to inser
            self.__growExistingClusterInAClusterList(row, clusterIdx)
        else: # cosine similarity is low, so we create new cluster
            new_cluster = Cluster()
            new_cluster.addOneRowToCluster(row)
            self.__addNewClusterToClusterList(new_cluster)

        if blockingTurnedOn: #keep the indexing dictionary up to date
            self.indexer.updateIndexingDict()


    def __str__(self) -> str:
        returnedStr = "\n" + "largestOccupiedIndex : " + str(self.nextAvailIndex-1) +  "\n" + "cluster aggr function: " + str(self.clusterAggrFunction) + "\n" +"clusterReps: " + str(self.clusterAggregations) +"\n"+"numberOfItemsInEachCluster: ["

        for cluster in self.clusterList:
            returnedStr = returnedStr + str(cluster.getNumberOfStoredRows()) + ", "

        returnedStr = returnedStr + "]"
        return returnedStr
    


