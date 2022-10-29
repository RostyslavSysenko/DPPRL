import sys, os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.ClusterList import ClusterList

class results:
    """
    This class is for saving clusterList in a file and loading one into memory.
    Future work might include allowing for different filenames using an input parameter.
    """
    def __init__(self):
        self.saveFilenameC = "./outputs/ClusterOutputs.txt"
        self.saveFilenameClist = "./outputs/ClusterListOut.txt"

    def saveClusterList(self, ClusterList):
        
        print(ClusterList, file=open(self.saveFilenameClist, "a"))


    def saveClusters(self, ClusterList):
        for cluster in ClusterList.clusterList:
            print(cluster, file=open(self.saveFilenameC, "a"))


    def loadClusterList(self, linkageUnit):
        fileCList = open(self.saveFilenameClist)
        fileClus = open(self.saveFilenameC)
        # Convert to string
        CListString = fileCList.readlines()
        assert type(CListString) == str

        # Send to ClusterList module
        linkageUnit.clusterlist.loadFromFile(CListString)
        linkageUnit.clusterlist.buildFromFile(fileClus)

    
