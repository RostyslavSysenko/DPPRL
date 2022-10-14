from array import *
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from data_structures.Indixer import * # Indexer
from data_structures.ClusterList import * # Indexer

class ClusterList:
    def __init__(self, certaintyThreshold = 0.5,clusterAggrFunction = AggrFunct.MEAN,indexer = None):
        '''
        Indexer: when ClusterList is created, if indexer is passed as input then dynamic insertion will be done using the indexer.
        Else, no blocking/indexing will be done and the performance might be slower
        '''
        
        self.nextAvailIndex = 0
        self.certaintyThreshold = certaintyThreshold
        self.clusterAggrFunction =clusterAggrFunction
        self.clusterList = []
        self.clusterAggregations = []; # 2d array of clusters and each cluster array contains 0/1 bit encodings        
        
        self.__indexer = indexer #indixer

    def blockingTurnedOn(self):
        return self.__indexer is not None

    def listOfClustersTo2DArrayOfClustAggr(clusterList):
        clusterListRepr2D = list()

        for cluster in clusterList:
            clusterListRepr2D.append(cluster.getClusterListRepresentation())
            
        return clusterListRepr2D

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

    def __generateRowList(self):
        # output: a list of all rows across all clusters
        # ASSUMPTION: the assumption on which this method relies is that each row appears across all clusters only once.
        # this is a true assumption in this use case if other code has been written properly and no duplicate rows exist across clusters
        rowList = []

        for cluster in self.clusterList:
            assert type(cluster) == Cluster

            rowsFromCurrCluster = cluster.getClusterRowObjList()
            rowList = rowList + rowsFromCurrCluster

        return rowList

    def addRowDynamic(self, row):
        # this is an implimentation of dynamic linkage which refits the model every time a dynamic linkage is needed and then finds 1 NN based on that newly created model
        # we assume the order of clusers never changes (meaning clusters are never deleted or reordered)
        from clustering.DynamicClustering import DynamicClusterer

        if(self.blockingTurnedOn() and self.__indexer.indexingHasNotBeenDoneYet()):
            rowList = self.__generateRowList()
            self.__indexer.initialIndexBuild(rowList)
    
        clusterIdx,selectionCertainty = DynamicClusterer.findBestClusterForRow(self.blockingTurnedOn(),row,Operation.INSERT, self.__indexer,self.clusterAggregations)

        # here we conduct the insertion operation
        if (selectionCertainty>self.certaintyThreshold): # we decide to inser
            self.__growExistingClusterInAClusterList(row, clusterIdx)
        else: # clustering certainty is low so we create a new cluster
            new_cluster = Cluster()
            new_cluster.addOneRowToCluster(row)
            self.__addNewClusterToClusterList(new_cluster)

        if self.blockingTurnedOn(): #keep the indexing dictionary up to date
            self.__indexer.updateIndexingDictOnInsert(insertedRow=row)


    def __str__(self) -> str:
        returnedStr = "\n" + "largestOccupiedIndex : " + str(self.nextAvailIndex-1) +  "\n" + "cluster aggr function: " + str(self.clusterAggrFunction) + "\n" +"clusterReps: " + str(self.clusterAggregations) +"\n"+"numberOfItemsInEachCluster: ["

        for cluster in self.clusterList:
            returnedStr = returnedStr + str(cluster.getNumberOfStoredRows()) + ", "
            

        returnedStr = returnedStr + "]"
        return returnedStr
    


