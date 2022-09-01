from array import *
import statistics

class ClusterList:
    def __init__(self,clusterList):
        self.clusterList = clusterList
        self.clusterRepresentations = []; # 2d array of clusters and each cluster array contains 0/1 bit encodings
    
    def addCluster(self, clusterRowsList):
        self.clusterList.append(Cluster(clusterRowsList,len(self.clusterList)))

    def initialClusterRepresentationCompile(self):
        clusterReps = []

        for cluster in self.clusterList:
            clusterRepresentation = cluster.setClusterRepresentationToMeanVector()
            clusterReps.append(clusterRepresentation)
        
        self.clusterRepresentations = clusterReps


class Cluster:
    def __init__(self,clusterRowsList,id):
        self.clusterId = id
        self.clusterRepresentation = None
        self.clusterRows = clusterRowsList

    def setClusterRepresentationToMeanVector(self):
        #assume cluster has at least 1 row
        assert len(self.clusterRows)>0

        meanVector = []
        arr2D = self.putRowEncodingsInto2DArrayDataStructure()

        rowsNum = len(arr2D)
        colsNum = len(arr2D[0])
        
        for j in range(0,colsNum):
            sum = 0
            n = 0

            for i in range(0,rowsNum):
                sum = sum + arr2D[i][j]
                n = n+1
            
            mean = sum/n
            meanVector.append(mean)
        
        self.clusterRepresentation = meanVector
        return meanVector

    def setClusterRepresentationToMedianVector(self):
        #assume cluster has at least 1 row
        assert len(self.clusterRows)>0

        medianVector = []
        arr2D = self.putRowEncodingsInto2DArrayDataStructure()
        
        for j in range(0,len(arr2D[0])):
            colVector = []
            for i in range(0,len(arr2D)):
                colVector.append(arr2D[i][j])

            median = statistics.median(colVector)
            medianVector.append(median)
        
        self.clusterRepresentation = medianVector

    
    def putRowEncodingsInto2DArrayDataStructure(self):
        return [[int(digit) for digit in row.encodedRowString] for row in self.clusterRows]


class Row:
    def __init__(self,encodedRow):
        self.encodedRowString = encodedRow




## ---------------------------------------
## Some basic testing
listOfRows = [  Row("000"),
                Row("222"),
                Row("999")]
cluster = Cluster(listOfRows)

## test 1
cluster.setClusterRepresentationToMeanVector()
print(cluster.clusterRepresentation)

## test 2
cluster.setClusterRepresentationToMedianVector()
print(cluster.clusterRepresentation)





listOfRows = [
        Row("000"),
        Row("111")]

cluster = Cluster(listOfRows)

## test 3
cluster.setClusterRepresentationToMeanVector()
print(cluster.clusterRepresentation)

## test 4
cluster.setClusterRepresentationToMedianVector()
print(cluster.clusterRepresentation)