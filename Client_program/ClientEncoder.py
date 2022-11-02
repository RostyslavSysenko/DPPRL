import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
from Modules.argumentHandler import argumentHandler
from Modules.ClientCommunicator import ClientCommunicator
from Modules.FileEncoder import FileEncoder
import time
import subprocess


class ClientEncoder:
    """
    This class is designed to simulate the entire process by which multiple file encodings would be completed and sent to the server.
    Configurable settings and will initially be hardcoded for testing purposes.
    corruptionLevels = [0,20,40]
    sortedOrdering = [True, False] # Boolean ordered = True | False
    bloomFilterLengths = [20, 50, 100, 500]
    """
    def __init__(self,static,total, corruption=0,bfLen=50):
        self.corruptionLevel = corruption
        self.bloomFilterLength = bfLen
        self.port = 43555 # Add as an argument later, not necessary since the networking part of this program is not the focus.

        self.numOfStaticClients = static # Assumes these will be the first ones and all afterwards (up to total) are dynamic.
        self.numOfClients = total

    def runClient(self, filePath,static=False):
        argHandler = argumentHandler()
        bf = argumentHandler.bloomFilterOfLength(self.bloomFilterLength)
        comm = ClientCommunicator()
        fileEnc = FileEncoder(bf,comm)#,argHandler=argHandler)
        fileEnc.fileLocation = filePath
        fileEnc.attributeTypesList = argHandler.defineAttributeTypes(typesList="NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED")
        fileEnc.loadFile()
        fileEnc.nameAttributes()#argHandler)
        fileEnc.encodeAllRecords(bf)     
        
        # Attempt to connect to the server
        fileEnc.communicator.connectToServer('127.0.0.1', self.port)  
        if static:
            fileEnc.sendEncodingsStatic()
        else:
            fileEnc.sendEncodingsDynamic()
        return fileEnc

    def findFilePath(corruption, number):
        locationString = "./datasets_synthetic/ncvr_numrec_500_modrec_2_ocp_" + str(corruption) + "_myp_" + str(number) + "_nump_5.csv"
        print("Using file:", locationString)
        return locationString

    def runAllClients(self):
        for i in range(0,self.numOfClients):
            datasetPath = ClientEncoder.findFilePath(self.corruptionLevel,i)
            if i < self.numOfStaticClients:
                client = self.runClient(datasetPath, static=True)           
            else: 
                client = self.runClient(datasetPath)
            
            if i+1 == self.numOfStaticClients:
                # If last static client then wait for staticlinkage to complete before continuing to dynamic
                client.communicator.send("STATIC LINK")
                client.communicator.waitForAcknowledge()

    def tellServer(self, message):
        communication = ClientCommunicator()
        communication.connectToServer('127.0.0.1', self.port)
        communication.send(message)

            

def main():
    # Program Usage: ClientEncoder.py staticDatasets totalDatasets corruption bloomfilterLength
    if len(sys.argv)<5:
        print("Not enough arguments")
        print("Program Usage: ClientEncoder.py staticDatasets totalDatasets corruption bloomfilterLength")
        sys.exit(1)
    elif len(sys.argv)>5:
        print("Too many arguments")
        print("Program Usage: ClientEncoder.py staticDatasets totalDatasets corruption bloomfilterLength")

    # Receive arguments
    staticCount = int(sys.argv[1])
    total = int(sys.argv[2])
    corruption = int(sys.argv[3])
    bfLen = int(sys.argv[4])

    # Initialise program
    encoders = ClientEncoder(staticCount,total,corruption=corruption,bfLen=bfLen)
    encoders.runAllClients()

    # encoders.tellServer("SAVECLUSTERS")
    encoders.tellServer("METRICS")
    encoders.tellServer("QUIT")
    time.sleep(2)
    
    




    

if __name__ == "__main__":
    main()
