import sys, os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.ClusterList import ClusterList
import pickle

class results:
    """
    This class is for saving clusterList in a file and loading one into memory.
    Future work might include allowing for different filenames using an input parameter.
    """
    def __init__(self):
        self.saveFilenameC = "./outputs/ClusterOutputs.pkl"
        self.saveFilenameClist = "./outputs/ClusterListOut.pkl"

    def saveClusterList(self, ClusterList):
        """
        saves a pickle byte string that is built based on its pickle representation. This is needed so that the state of the program can be
        saved into hard disc or used for analytics
        """
        file = open(self.saveFilenameClist, 'wb')
        pickle.dump(ClusterList, file)

    def loadClusterList(self, linkageUnit):
        """
        returns a cluster list that is built based on its pickle representation.
        """
        fileCList = open(self.saveFilenameClist, "rb")
        linkageUnit.clusterlist = pickle.load(fileCList)
        print("Loaded server using imported clusterlist of length:",len(linkageUnit.clusterlist.clusterList))

