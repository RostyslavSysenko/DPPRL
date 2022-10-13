from array import *
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from data_structures.Indixer import * # Indexer
from clustering.DynamicClustering import *

class ClusterList:
    def __init__(self, certaintyThreshold = 0.5,clusterAggrFunction = AggrFunct.MEAN,indexingBitStart=None, indexingBitEnd = None ):
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
    


