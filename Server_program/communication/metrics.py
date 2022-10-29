import os, sys
from Server_program.data_structures.Utilities import Cluster
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.ClusterList import ClusterList


class metrics:
    """
    This class stores and finds metrics relating to the linkage unit.
    """
    def __init__(self, server):
        self.linkageUnit = server # Use for access to all realtime data on the linkage unit
        # Metrics being looked for
        self.frequencyAttackCorrectGuesses = 0
        self.averageClusterPurity = 0.0 # Aim: 1
        self.perfectClustersPercent = 0 #in range(0, 100) # Aim: 100
        self.clustersWithMatches = 0 # Aim: 2500.

        # Unsure what is BigO space & Time (Space/Time complexity?)
        self.linkageRuntimes = [] # List of all/any calculated linkage runtimes

        # Data needed in memory for metric calculation
        self.initialRuntime = 0

        # Average runtime for dynamic insert
        self.dynamicRuntimes = []

        self.clusterList = None

    def update(self):
        self.findAverageClusterPurity()
        self.findPerfectClusterPercentage()
        self.findClustersWithMatches()

    def display(self): 
        # Print metrics to the server console
        print("Average Cluster Purity:", self.averageClusterPurity)
        print("Perfect Clusters: ", self.perfectClustersPercent)
        print("Clusters with matches: ", self.clustersWithMatches)

    def displayLatest(self):
        self.update()
        self.display()

    def updateClusters(self,clustList):
        self.clusterList = clustList

    def findAverageClusterPurity(self,averageClusterPurity):
        # 

       # contingency_matrix = metrics.cluster.contingency_matrix(averageClusterPurity, ClusterList)
# return purity
       # return sum(amax (contingency_matrix, axis=0)) / sum(contingency_matrix)


        pass

    def findPerfectClusterPercentage(self):
        # 

        pass

    def findGroundTruth(self,rowLists):
        # Computing the ground truth clusterlist using rec_id's.
        # Find unique rec_ids
        uniqueRowIds = []
        clusters = []
        for rowList in rowLists:
            for row in rowList:
                rec_id = row.rowId
                if rec_id not in uniqueRowIds:
                    uniqueRowIds.append(row.rowId)                  

        print("Number of unique rec_ids:",len(uniqueRowIds))
        # Create clusters for each unique rec_id and populate those clusters.
        for id in uniqueRowIds:
            cluster = Cluster(id)
            for rowList in rowLists:
                for row in rowList:
                    if row.rowId == id:
                        cluster.addOneRowToCluster(row)
            clusters.append(cluster)

        print("Found",len(clusters),"matches using rec_id for ground truth")

    def averageDynamicRuntime(self):
        total = 0
        for runtime in self.dynamicRuntimes:
            total += runtime

        dynamicInsertionCount = len(self.dynamicRuntimes)
        average = total / dynamicInsertionCount
        return average

    def startDynamicInsert(self):
        currentRuntime = self.linkageUnit.runtime()
        # Store current runtime in memory.
        self.initialRuntime = currentRuntime

    def finishDynamicInsert(self):
        currentRuntime = self.linkageUnit.runtime()
        insertTime = currentRuntime - self.initialRuntime
        self.dynamicRuntimes.append(insertTime)

        dynamicInsertionCount = len(self.dynamicRuntimes)

        if dynamicInsertionCount % 500 == 0:
            averageDynamicTime = self.averageDynamicRuntime()

            print("Average dynamic insertion time:", averageDynamicTime)
 

    def findClustersWithMatches(self):
        # Count number of clusters with between 2 and 5 rows in them
        assert type(self.clusterList) == ClusterList

        clusterWithMatches = 0
        for cluster in self.clusterList.clusterList:
            rowCount = cluster.getNumberOfStoredRows()
            if (rowCount >= 2) | (rowCount <= 5):
                clusterWithMatches += 1

        self.clustersWithMatches = clusterWithMatches
        print(clusterWithMatches)
        return clusterWithMatches

    def beginLinkage(self):
        currentRuntime = self.linkageUnit.runtime()
        # Store current runtime in memory.
        self.initialRuntime = currentRuntime

    def finishLinkage(self):
        currentRuntime = self.linkageUnit.runtime()
        linkageTime = currentRuntime - self.initialRuntime
        self.linkageRuntimes.append(linkageTime)
        print("LINKAGE RUNTIME: ", linkageTime)
        return linkageTime

        
