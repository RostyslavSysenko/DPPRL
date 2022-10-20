import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
#from server import Server

"""
This class stores and finds metrics relating to the linkage unit.

"""



class metrics:
    def __init__(self, server):
        self.linkageUnit = server # Use for access to all realtime data on the linkage unit
        # Metrics being looked for
        self.frequencyAttackCorrectGuesses = 0
        self.averageClusterPurity = 0.0 # Aim: 1
        self.perfectClustersPercent = 0 #in range(0, 100) # Aim: 100
        self.clustersWithMatches = 0 # Aim: 2500.

        # Unsure what is BigO space & Time?
        self.linkageRuntimes = [] # List of all/any calculated linkage runtimes

        # Data needed in memory for metric calculation
        self.initialRuntime = 0

    def update(self):
        self.findAverageClusterPurity()
        self.findPerfectClusterPercentage()
        self.findClustersWithMatches

    def display(self): 
        # Print metrics to the server console
        print("Average Cluster Purity:", self.averageClusterPurity)
        print("Perfect Clusters: ", self.perfectClustersPercent)

    def displayLatest(self):
        self.update()
        self.display()

    def findAverageClusterPurity(self):
        # 

        pass

    def findPerfectClusterPercentage():
        # 

        pass

    def findClustersWithMatches(self):
        # Number of clusters with between 2 and 5 rows in them
        
        pass

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

        
