from array import *
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from data_structures.Indixer import * # Indexer
#from clustering.DynamicClustering import *

class ClusterList:
    """
    Guide on how to use this class:
    - this class is to be used inside the server program on a linkage unit
    - this class needs to be instantiated once only and will contain the linkage for records across all databases
    - when using this class, a user would usually want to instantiate an Indexer object from a class that we provided
    and pass it into ClusterList since doing so would allow would allow for multi stage indexing and hopefully good speed up on the linkage
    - Note: clusterList can be used without Indexer and will work just fine, it will just usually be slower, but linkage might be improved
    in quality.
    - After cluster list is created, the cluster list would need to be populated statically using addClusterStaticly(clusterObj) function.
    Please note that to populate the clusterList, user needs to already have a set of clusters and rows corresponding to those clusters.
    This set of clusters with corresponding rows can be generated using our static linkage module (created by Amanda). Then those generated
    clusters and lists need to be converted into appropriate format and inserted into cluster list one by one using addClusterStaticly(clusterObj). 
    The use case for that function can be found inside the testing file for data structures 
    - then once the clusterList is set up we could insert rows dynamically into it using addRowDynamic(row) which would do the insertion
    - use cases of how cluster list can be used can be found inside the testing folder (tests make extensive use of both clusterList and Indexer classes)
    """
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
        """
        input: valid Cluster object (class for cluster can be found inside the Utilities folder i think). The cluster should have at least one 
        row in it already, else it doesnt make sense to have empty cluster
        
        output: the output is that a cluster gets integrated into a cluster list at latest index (i think)
        """
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

    def addRowDynamic(self, row, DynamicClusterer):
        """ 
        input: Row object (which is found in Utilities folder i think)

        output: nothing gets printed or returned and instead the row gets integrated into the ClusterList data structure

        More info: this is an implimentation of dynamic linkage which refits the model every time a dynamic linkage is needed and then finds 1 NN based on that newly created model
        we assume the order of clusers never changes (meaning clusters are never deleted or reordered)
        from clustering.DynamicClustering import DynamicClusterer
        """

        if(self.blockingTurnedOn() and self.__indexer.indexingHasNotBeenDoneYet()):
            rowList = self.__generateRowList()
            self.__indexer.initialIndexBuild(rowList)
    
        clusterIdx,selectionCertainty = DynamicClusterer.findBestClusterForRow(self.blockingTurnedOn(), row, Operation.INSERT, self.__indexer, self.clusterAggregations)

        # here we conduct the insertion operation
        if (selectionCertainty>self.certaintyThreshold): # we decide to insert
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
    


