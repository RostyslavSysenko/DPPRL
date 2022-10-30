import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.ClusterList import ClusterList
from data_structures.Utilities import Cluster
import matplotlib.pyplot as plt
from sklearn import metrics as skmetrics

class metrics:
    """
    This class stores and finds metrics relating to the linkage unit.
    """
    def __init__(self, server):
        self.linkageUnit = server # Use for access to all realtime data on the linkage unit
        # Metrics being looked for
        self.frequencyAttackCorrectGuesses = 0
        self.averageClusterPurity = 0.0
        self.perfectClustersPercent = 0
        self.clustersWithMatches = 0

        # Unsure what is BigO space & Time (Space/Time complexity?)
        self.linkageRuntimes = [] # List of all/any calculated linkage runtimes

        # Data needed in memory for metric calculation
        self.initialRuntime = 0
        self.groundTrueClusters = None
        self.dynamicRuntimes = [] # Average runtime for dynamic insert

    def update(self):
        scoreslist = self.computeAllClusterPurities()
        self.averageClusterPurity = self.getAveragePurity(scoreslist)
        self.perfectClustersPercent = self.getPerfectPurityPercentage(scoreslist)
        self.clustersWithMatches = self.findNumberOfClustersWithAtLeastNRows(2)
        
    
    def display(self): 
        # Print metrics to the server console
        print("Average Cluster Purity:", self.averageClusterPurity)
        print("Perfect Clusters: ", self.perfectClustersPercent)
        print("Clusters with matches: ", self.clustersWithMatches)

        metrics.displayDynamicInsertionTimeTrend(self.dynamicRuntimes)
        metrics.getPurityDistribution(self.computeAllClusterPurities())

    def displayLatest(self):
        self.update()
        self.display()

    def displayDynamicInsertionTimeTrend(dynamicRuntimes):
        # outputs a trend plot showing how the performance of insertion changes as more rows get inserted
        numOfDivisions = 10
        divisionSize = len(dynamicRuntimes)/numOfDivisions

        listOfDivisionAverages = []
        counts = [i for i in range(0,numOfDivisions)]

        for i in range(0,numOfDivisions):
            startIdx = int(i*divisionSize)
            endIdx = int((i+1)*divisionSize)
            dision_i_sublist  = dynamicRuntimes[startIdx:endIdx]
            avr_division_i = sum(dision_i_sublist)/len(dision_i_sublist)
            listOfDivisionAverages.append(avr_division_i)
        
        plt.plot(counts, listOfDivisionAverages)
        plt.title(f"Time it takes on average to complete 1 dynamic insertion when ~= i*{divisionSize} records already dynamically inserted")
        plt.xlabel("i")
        plt.ylabel("avr time")
        plt.show() 

    def getPerfectPurityPercentage(self,purityScoresList):
        ttl = 0
        pureNum = 0 
        for score in purityScoresList:
            ttl = ttl+1
            if score ==1:
                pureNum= pureNum+1
                
        self.perfectClustersPercent =  pureNum/ttl

    def getAveragePurity(self,purityScoresList):
        
        self.averageClusterPurity = sum(purityScoresList)/len(purityScoresList)

    def getPurityDistribution(purityScoreList):

        distributionSegments = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90-100"]
        frequencyBySegment = [0 for i in range(0,10)]

        for score in purityScoreList:
            scoreSegment = (int)*score/10

            if(scoreSegment==10):
                scoreSegment=9
            
            frequencyBySegment[scoreSegment] = frequencyBySegment[scoreSegment]+1
        
        plt.plot(distributionSegments, frequencyBySegment)
        plt.title(f"Distribution of Cluster's assigned correctness")
        plt.xlabel("purity score (%)")
        plt.ylabel("frequency")
        plt.show() 
     
    
    def computeAllClusterPurities(self):
        ourClusterList = self.linkageUnit.clusterlist.clusterList
        scoreList = []

        for cluster in ourClusterList:
            score = self.getPurityScore(cluster)
            scoreList.append(score)
        
        return scoreList
    
    def getPurityScore(self, linkedCluster):
        """
        For each row in input cluster, find corresponding clusters in the ground truth dataset.
        If corresponding clusters are the same, increment for each. Divide by total rows.
        
        """
        totalRows = linkedCluster.getNumberOfStoredRows()
        # Will be calling cluster methods on input
        assert type(linkedCluster) == Cluster
        
        # Find ground truth if not done already.
        if (self.groundTrueClusters == None) | (len(self.groundTrueClusters) <= 1):
            self.linkageUnit.findGroundTruth()

        # Find corresponding clusters in ground truth, if they contain a common row to our input then add them to the list
        correspondingClusters = []
        for linkedRow in linkedCluster.getClusterRowObjList(): # Loop through cluster rows
            foundRowInGroundTruth = False
            for groundTrueCluster in self.groundTrueClusters: # Ground truth clusters
                if linkedCluster.getClusterRowObjList() == groundTrueCluster.getClusterRowObjList():
                    return 1 # If there is a ground true cluster with exact same rows then return 1

                if foundRowInGroundTruth:
                    break
                
                for trueRow in groundTrueCluster.getClusterRowObjList(): # If a row is common
                    if linkedRow.rowId == trueRow.rowId:
                        correspondingClusters.append(groundTrueCluster)
                        foundRowInGroundTruth = True
                        break
        
        #print(correspondingClusters)
        # list of clusters, each has at least one row same as input cluster
        # trying to find highest frequency cluster
        highestfrequency = 0
        highestFreqCluster = None
        for cluster in correspondingClusters:
            frequency = 0
            # Loop through every other cluster 
            for otherCluster in correspondingClusters:
                if correspondingClusters.index(cluster) == correspondingClusters.index(otherCluster):
                    continue # to avoid 
                elif cluster == otherCluster:
                    frequency += 1
            if frequency > highestfrequency:
                highestfrequency = frequency
                highestFreqCluster = cluster        
        
        return highestfrequency / totalRows
    

    def updateGroundTruthClusters(self):
        # Create list of rowLists using ClusterList
        ourClusterList = self.linkageUnit.clusterlist.clusterList
        


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

        #matches = self.findClustersWithMatches(clusters)
        print("Generated",len(clusters),"ground truth clusters.")
        self.groundTrueClusters = clusters

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
 

    def findNumberOfClustersWithAtLeastNRows(self,n):
        # Count number of clusters with between 2 and 5 rows in them
        clusterListOnServer = self.linkageUnit.clusterlist
        assert type(clusterListOnServer) == ClusterList

        clusterWithMatches = 0
        for cluster in clusterListOnServer.clusterList:
            rowCount = cluster.getNumberOfStoredRows()
            if (rowCount >= n):
                clusterWithMatches += 1

        self.clustersWithMatches = clusterWithMatches
        return clusterWithMatches # int

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

        
