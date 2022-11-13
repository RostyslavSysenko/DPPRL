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
        self.scoreslist = []
        self.clusterCount = 0

    def update(self):
        self.scoreslist = self.computeAllClusterPurities()
        #print(self.scoreslist)
        self.getAveragePurity(self.scoreslist)
        self.getPerfectPurityPercentage(self.scoreslist)
        self.clustersWithMatches = self.findNumberOfClustersWithAtLeastNRows(2)
        
    
    def display(self): 
        # Print metrics to the server console
        print("Average Cluster Purity:", self.averageClusterPurity)
        print("Perfect Clusters: ", self.perfectClustersPercent)
        print("Clusters with matches: ", self.clustersWithMatches)
        self.graphs()
        self.linkageUnit.shutdown()

    def graphs(self):
        metrics.displayDynamicInsertionTimeTrend(self.dynamicRuntimes)
        metrics.getPurityDistribution(self.scoreslist)
        self.clusterSizeDistribution()

    def displayLatest(self):
        self.update()
        self.display()

    def displayDynamicInsertionTimeTrend(dynamicRuntimes):
        # outputs a trend plot showing how the performance of insertion changes as more rows get inserted
        numOfDivisions = 20
        divisionSize = len(dynamicRuntimes)/numOfDivisions

        listOfDivisionAverages = []
        counts = [i*divisionSize for i in range(0,numOfDivisions)]

        for i in range(0,numOfDivisions):
            startIdx = int(i*divisionSize)
            endIdx = int((i+1)*divisionSize)
            dision_i_sublist  = dynamicRuntimes[startIdx:endIdx]
            if len(dision_i_sublist) != 0:
                avr_division_i = sum(dision_i_sublist)/len(dision_i_sublist)
            else:
                avr_division_i = 0 # If dynamic insertions have not been completed or recorded
            listOfDivisionAverages.append(avr_division_i)
        
        plt.plot(counts, listOfDivisionAverages)
        plt.title(f"Time it takes on average to complete 1 dynamic insertion when i records already dynamically inserted")
        plt.xlabel("Number of records already dynamically inserted")
        plt.ylabel("avr time")
        plt.show() 

    def getPerfectPurityPercentage(self,purityScoresList):
        ttl = 0
        pureNum = 0 
        for score in purityScoresList:
            ttl = ttl+1
            if score == 100:
                pureNum= pureNum+1
                
        self.perfectClustersPercent =  pureNum/ttl

    def getAveragePurity(self,purityScoresList):
        
        self.averageClusterPurity = sum(purityScoresList)/len(purityScoresList)

    def getPurityDistribution(purityScoreList):

        distributionSegments = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90-100"]
        frequencyBySegment = [0 for _ in range(0,10)]

        for score in purityScoreList:
            scoreSegment = int(score/10)

            if(scoreSegment==10):
                scoreSegment=9
            
            frequencyBySegment[scoreSegment] = frequencyBySegment[scoreSegment]+1
            
        ttlCluster = sum(frequencyBySegment)
        probabilityBySegment = [frequencyOfCluster/ttlCluster for frequencyOfCluster in frequencyBySegment]

        plt.bar(distributionSegments, probabilityBySegment)
        plt.title(f"Distribution of Cluster's linkage correctness")
        plt.xlabel("purity score (%)")
        plt.ylabel("probability")
        plt.show() 

    def clusterSizeDistribution(self):
        ourClusterList = self.linkageUnit.clusterlist.clusterList

        clusterSizeList = [cluster.getNumberOfStoredRows() for cluster in ourClusterList]

        plt.hist(clusterSizeList,rwidth = 0.7)
        plt.xlabel('Row count inside cluster')
        plt.ylabel('frequency')
        plt.show()
        plt.show()
     
    
    def computeAllClusterPurities(self):
        ourClusterList = self.linkageUnit.clusterlist.clusterList
        self.clusterCount = len(ourClusterList)
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
        # Will be calling cluster methods on input
        assert type(linkedCluster) == Cluster
        totalRows = linkedCluster.getNumberOfStoredRows()
        linkedRows = linkedCluster.getClusterRowObjList()
        
        # Find ground truth if not done already.
        if self.groundTrueClusters == None:
            self.updateGroundTruthClusters()
        elif len(self.groundTrueClusters) <= 1:
            self.updateGroundTruthClusters()

        # Find corresponding clusters in ground truth, if they contain a common row to our input then add them to the list
        correspondingClusters = []
        for linkedRow in linkedRows: # Loop through cluster rows
            for groundTrueCluster in self.groundTrueClusters: # Ground truth clusters
                if linkedRows == groundTrueCluster.getClusterRowObjList():                  
                    return 100 # If there is a ground true cluster with exact same rows in same order then return 100%
            foundCluster = self.findRowInGroundTruth(linkedRow)
            correspondingClusters.append(foundCluster)                
        
        
        # list of clusters, each has at least one row same as input cluster
        # trying to find highest frequency cluster
        highestfrequency = 0
        highestFreqCluster = None
        for cluster in correspondingClusters:
            frequency = correspondingClusters.count(cluster)
            if frequency > highestfrequency:
                highestfrequency = frequency
                highestFreqCluster = cluster

        if highestfrequency == 1:
            return 0

        for row in highestFreqCluster.getClusterRowObjList():
            matchedRows = 0
            for matchedRow in linkedRows:
                if row.rowId == matchedRow.rowId:
                    matchedRows += 1

        purityScore = (matchedRows / totalRows) * 100
        #print("PurityScore:",purityScore,linkedCluster)
        return purityScore # percentage 

    def clusterRowsMatchFraction(cluster, secondCluster):
        assert type(cluster) == Cluster
        numberofRows = cluster.getNumberOfStoredRows()     
        match = 0  
        for row in cluster.getClusterRowObjList():
            for srow in secondCluster.getClusterRowObjList():
                #print(row.rowId,srow.rowId)
                if row.rowId == srow.rowId:
                    match += 1
                    #print("matched")

        matchScore = match / numberofRows
        #print(matchScore)
        return matchScore

    def findRowInGroundTruth(self,row):
        foundCluster = None
        for groundTrueCluster in self.groundTrueClusters: # All ground truth clusters
            for trueRow in groundTrueCluster.getClusterRowObjList(): # Compare every row in ground truth to input
                if row.rowId == trueRow.rowId: # Find the row based on rec_id
                    foundCluster = groundTrueCluster
                    return foundCluster                
        if foundCluster == None:
            print("Metrics error! Row not found in ground truth cluster list")
        return foundCluster
    

    def updateGroundTruthClusters(self):
        # Create list of rowLists using ClusterList
        ourClusterList = self.linkageUnit.clusterlist.clusterList
        Dbs = self.clusterListToRowLists(ourClusterList)
        clusters = []
        
        # Computing the ground truth clusterlist using rec_id's.
        # Find unique rec_ids
        uniqueRowIds = self.findUniqueRecIds(Dbs)              

        print("Number of unique rec_ids:",len(uniqueRowIds))
        # Create clusters for each unique rec_id and populate those clusters.
        for id in uniqueRowIds:
            cluster = Cluster(id)
            for rowList in Dbs:
                for row in rowList:
                    if row.rowId == id:
                        cluster.addOneRowToCluster(row)
            clusters.append(cluster)

        #matches = self.findClustersWithMatches(clusters)
        print("Generated",len(clusters),"ground truth clusters.")
        self.groundTrueClusters = clusters

    def findUniqueRecIds(self,Dbs):
        # Takes in list of list of rows
        uniqueRowIds = []
        for rowList in Dbs:
            for row in rowList:
                rec_id = row.rowId
                if rec_id not in uniqueRowIds:
                    uniqueRowIds.append(row.rowId)    

        return uniqueRowIds

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

    def findUniqueDbIds(self,AllRows):
        # Takes in list of list of rows
        uniqueRowIds = []    
        for row in AllRows:
            DbId = row.DbId
            if DbId not in uniqueRowIds:
                uniqueRowIds.append(row.DbId)    

        return uniqueRowIds

    def clusterListToRowLists(self, clusterList):        
        # Takes in actual list of clusters    
        AllRows = []
        # First populate AllRows with all rows in all clusters
        for cluster in clusterList:
            assert type(cluster) == Cluster
            clusterRows = cluster.getClusterRowObjList()
            for row in clusterRows:
                AllRows.append(row)

        uniqueDbIds = self.findUniqueDbIds(AllRows)
        #print(uniqueDbIds)

        # Find highest id and populate RowLists with empty lists up to highestId - 1
        RowLists = []
        highestId = 0
        for id in uniqueDbIds:
            if id == 0:
                print("Error imminent: DB of id 0, index -1 will not exist.")
            if id > highestId:
                highestId = id
        # Highest id number has been found.

        for i in range(0,highestId):
            Db = []
            RowLists.append(Db)
        # Result is empty lists from indexes 0 to highestId - 1

        #print(RowLists)

        # Then split AllRows based on row.DbId into lists at index DbId-1 inside of RowLists.
        for row in AllRows:
            DbIndex = row.DbId-1
            RowLists[DbIndex].append(row)
            
        return RowLists

