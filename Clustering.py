from array import *
import statistics
from sklearn.neighbors import NearestNeighbors

class ClusterList:
    def __init__(self, clusterAggrFunction = "mean"):
        self.largestCurrentIdx = 0
        self.clusterAggrFunction =clusterAggrFunction
        self.clusterList = []
        self.clusterRepresentations = []; # 2d array of clusters and each cluster array contains 0/1 bit encodings
        self.knn_classifier = NearestNeighbors(n_neighbors=1, metric="cosine")

    def __addNewClusterToClusterList(self,clusterObj):
        clusterObj.updateParentClusterListRef(self)
        self.clusterRepresentations.append(clusterObj.clusterVecRepresentation)
        self.clusterList.append(clusterObj)

    def __growExistingClusterInAClusterList(self,rowBitString, clusterIdxToWhichWeAdd):
        self.clusterList[clusterIdxToWhichWeAdd].addToCluster(rowBitString) #CLUSTER gets updated
        self.clusterRepresentations[clusterIdxToWhichWeAdd] = self.clusterList[clusterIdxToWhichWeAdd].clusterRepresentation

    def addClusterStaticly(self,clusterObj):
        # this method is implimented for readability
        self.__addNewClusterToClusterList(self,clusterObj)

    def addRowDynamic(self, rowBitString):
        # we assume the order of clusers never changes (meaning clusters are never deleted or reordered)
        encodingArr = [int(char) for char in rowBitString]

        self.knn_classifier.fit(self.clusterRepresentations)
        distance_mat, neighbours_vec = self.knn_classifier.kneighbors([encodingArr])
        clusterIdx= neighbours_vec[0][0] # gets us index of cluster that we want to modify
        cosineSimilarity = 1 - distance_mat[0][0]

        if (cosineSimilarity > 0.8): # cosine similarity is high 
            self.growExistingClusterInAClusterList(rowBitString, clusterIdx)
        else: # cosine similarity is low 
            idx = self.largestCurrentIdx +1
            rowLst = [Row(rowBitString)]
            new_cluster = Cluster(rowLst,idx)
            self.addNewClusterToClusterList(new_cluster)
        return clusterIdx
    

class Cluster:
    def __init__(self,id,clusterAggFunction = None):
        self.__clusterId = id
        self.__parentClusterListObj = None

        self.__clusterRowObjLst = []
        self.__clusterVecAggr = []

    def __getAggrFunction(self):
        return self.__parentClusterListObj.clusterAggrFunction

    def __getRowNum(self):
        return len(self.__clusterRowObjLst)
    
    def __getAttributeNum(self):
        return len(self.__clusterRowObjLst[0].rowListRepresentation)

    def __setClusterAggrToMeanVector(self):
        #assume cluster has at least 1 row
        assert len(self.clusterRowObj)>0

        meanVector = []
        rowsNum = self.__getRowNum()
        colsNum = self.__getAttributeNum()
        
        for j in range(0,colsNum):
            sum = 0
            n = 0

            for i in range(0,rowsNum):
                sum = sum + self.__clusterRowObjLst[i].rowListRepresentation[j]
                n = n+1
            
            mean = sum/n
            meanVector.append(mean)
        
        self.__clusterVecAggr = meanVector

    def __setClusterAggrToMedianVector(self):
        #assume cluster has at least 1 row
        assert len(self.clusterRowObj)>0

        medianVector = []
        
        for j in range(0,self.__getAttributeNum()):
            colVector = []
            for i in range(0,self.__getRowNum()):
                colVector.append(self.__clusterRowObjLst[i].rowListRepresentation[j])

            median = statistics.median(colVector)
            medianVector.append(median)
        
        self.__clusterVecAggr = medianVector

    def updateParentClusterListRef(self,parentClusterListObjRef):
        self.__parentClusterListObj = parentClusterListObjRef

    def getId(self):
        return self.__clusterId

    def addOneToCluster(self, encodingString):
        self.__clusterRowObjLst.append(encodingString)

        if (self.__getAggrFunction() == "mean"):
            self.__setClusterAggrToMeanVector()
        if (self.__getAggrFunction() == "median"):
            self.__setClusterAggrToMedianVector()
        else:
            assert(False, "invalid aggregation function reached")

class Row:
    # non modifiable currently
    def __init__(self,encodedString):
        self.encodedRowString = encodedString
        self.rowListRepresentation = [int(char) for char in encodedString]






# -----------------TESTING------------------------
cList1 = ClusterList()
cList2 = ClusterList()

c1 = Cluster(0)
c1.addOneToCluster(Row("010"))
c1.addOneToCluster(Row("000"))
c1.addOneToCluster(Row("000"))

print("cluster1",c1)

c2 = Cluster(1)
c2.addOneToCluster(Row("111"))
c2.addOneToCluster(Row("111"))
c2.addOneToCluster(Row("110"))

print("cluster2",c2)

cList1.addNewCluster(c1)
cList1.addNewCluster(c2)

print("cList1 after 2x adding:",cList1)




