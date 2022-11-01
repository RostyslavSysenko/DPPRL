from http import server
import sys, os
from Server_program.communication.client import client
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from Server_program.server import Server
from Client_program.ClientEncoder import FileEncoder
from Client_program.ClientCommunicator import ClientCommunicator
from Client_program.argumentHandler import argumentHandler
import multiprocessing
import time
import subprocess
import tempfile
"""
Server Usage (Minimum usage from python):
server = Server(maxConns, sortedOrdering = True, similarityThreshold=, comparisonThreshold=)
server.setUpSocketOnCurrentMachine(port)
server.launchServer(loadingClusterList=argHandler.loadFromFile)
server.shutdown()
    

ClientEncoder Usage:
argHandler = argumentHandler(sys.argv)
    argHandler.handleArguments()
    bf = argHandler.findBloomFilterConfig()

    comm = ClientCommunicator()

    clientEncoder = FileEncoder(bf,comm,argHandler=argHandler)
    clientEncoder.nameAttributes(argHandler)
    clientEncoder.encodeAllRecords(bf)     

    
    # Attempt to connect to the server
    clientEncoder.communicator.connectToServer(argHandler.host, argHandler.port)  

    if not argHandler.dynamicLinkage:       
        # Send static insertions
        clientEncoder.sendEncodingsStatic()
        clientEncoder.communicator.send("SAVE") # Tell server to save the received encodings after finished sending.
        clientEncoder.communicator.waitForAcknowledge()

        if argHandler.staticLink: # This is sent on third dataset for demonstration (-l)
            clientEncoder.communicator.send("STATIC LINK")
    
    if argHandler.dynamicLinkage:
        # Send dynamic insertions
        clientEncoder.sendEncodingsDynamic()
        clientEncoder.communicator.send("SAVE") # Tell server to save the received encodings after finished sending.
        clientEncoder.communicator.waitForAcknowledge()

    # Close the socket and exit the program when all encodings have been sent.
    clientEncoder.communicator.soc.close()

def makeNewServer(sorted, simthresh,compthresh):
    port=43555
    maxConnections=15
    server = Server(maxConnections, sortedOrdering = sorted, similarityThreshold=simthresh, comparisonThreshold=compthresh)
    server.setUpSocketOnCurrentMachine(port)
    results = server.launchServer()
    #return server
    server.shutdown
    return results

def setOfFiveClients(port,bflen,corruption):
    # Connect all 5 clients
    c1 = newClient(port,bflen,filePath=fileLocation(corruption,1))
    c2 = newClient(port,bflen,filePath=fileLocation(corruption,2))
    c3 = newClient(port,bflen,filePath=fileLocation(corruption,3))
    c3.communicator.send("STATIC LINK")
    c4 = newClient(port,bflen,filePath=fileLocation(corruption,4), static=False)
    c5 = newClient(port,bflen,filePath=fileLocation(corruption,5), static=False)

    c1.communicator.soc.close()
    c2.communicator.soc.close()
    c3.communicator.soc.close()
    c4.communicator.soc.close()
    c5.communicator.soc.close()


def newClient(port,bloomfilterLen,filePath,static=True):
    argHandler = argumentHandler(filelocation=filePath)
    argHandler.defineAttributeTypes(typesList="NOT_ENCODED, STR_ENCODED, STR_ENCODED, STR_ENCODED, INT_ENCODED")
    bf = argumentHandler.bloomFilterOfLength(bloomfilterLen)
    comm = ClientCommunicator()
    clientEncoder = FileEncoder(bf,comm,argHandler=argHandler)
    
    clientEncoder.nameAttributes(argHandler)
    clientEncoder.encodeAllRecords(bf)     
    
    # Attempt to connect to the server
    clientEncoder.communicator.connectToServer('127.0.0.1', port)  
    if static:
        clientEncoder.sendEncodingsStatic()
    else:
        clientEncoder.sendEncodingsDynamic()
    return clientEncoder
"""
def fileLocation(corruption, number):
    locationString = "./Client_program/datasets_synthetic/ncvr_numrec_500_modrec_2_ocp_" + str(corruption) + "_myp_" + str(number) + "_nump_5.csv"
    return locationString

def clientScript(bflen,corruption):
    port = 43555
    print("running client program")

    programCall = "python -u ./Client_program/ClientEncoder.py " + fileLocation(corruption,0) + " " + str(bflen)
    proc = subprocess.Popen(programCall)
    proc.wait()
    programCall = "python -u ./Client_program/ClientEncoder.py " + fileLocation(corruption,1) + " " + str(bflen)
    proc = subprocess.Popen(programCall)
    proc.wait()
    programCall = "python -u ./Client_program/ClientEncoder.py -l " + fileLocation(corruption,2) + " " + str(bflen) + " " + str(port)
    proc = subprocess.Popen(programCall)
    proc.wait()
    time.sleep(6)
    programCall = "python -u ./Client_program/ClientEncoder.py -d " + fileLocation(corruption,3) + " " + str(bflen) + " " + str(port)
    proc = subprocess.Popen(programCall)
    proc.wait()
    programCall = "python -u ./Client_program/ClientEncoder.py -d " + fileLocation(corruption,4) + " " + str(bflen) + " " + str(port)
    proc = subprocess.Popen(programCall)
    proc.wait()
    programCall = "python -u ./Client_program/computeMetrics.py"
    time.sleep(30)
    proc = subprocess.Popen(programCall)

#def serverScript(ordered,statThres,dynThresh):   
    
    
def runExperiment(corruption,ordered,bflen,statThresh,dynThresh):
    if ordered:
        ordFunc = "-to "
    else:
        ordFunc = ""
    programCall = "python -u ./Server_program/server.py" + " " + ordFunc + str(15) + " " + str(statThresh) + " " + str(dynThresh) + " " + str(43555)
    avgPur = None
    perfClus = None

    with tempfile.TemporaryFile() as tempf:
        print("Starting server")
        proc = subprocess.Popen(programCall, stdout=tempf).communicate()[0]
        time.sleep(1)
        print("Starting client script")
        clientScript(bflen,corruption)
        proc.wait()
        tempf.seek(0)
        print( tempf.read())
    for line in tempf.readlines():
        
        if line.startswith("Average Cluster Purity: "):
            print(line)
            avgPur = line
        if line.startswith("Perfect Clusters: "):
            print(line)
            perfClus = line

    return avgPur, perfClus
    

#runExperiment(0,True,50,0.75,0.8)



# grid search optimising average purity percentage
time.sleep(20)
corruptionLevels = [0,20,40]
sortedOrdering = [True, False] # Boolean ordered = True | False
bloomFilterLengths = [20, 50, 100, 500]
comparThresholdDynamics = [0.7,0.8,0.9]
staticLinkageSimilarityThresholds = [0.7,0.8,0.9]

bestCorruptionLevel = corruptionLevels[0]
bestOrderingFunction = sortedOrdering[0]
bestBloomFIlterLEngth = bloomFilterLengths[0]
bestSimilarityThresholdDynamic = comparThresholdDynamics[0]
bestStaticLinkageSimilarityThreshold = staticLinkageSimilarityThresholds[0]

bestAveragePrityPercentage = 0
bestPerfPurityPercentage = 0


for staticLinkageSimilarityThreshold in staticLinkageSimilarityThresholds: # thrice
    print(staticLinkageSimilarityThreshold)
    for comparThresholdDynamic in comparThresholdDynamics: # thrice
        print(comparThresholdDynamic)
        for corruptionLevel in corruptionLevels: # thrice
            print(corruptionLevel)
            for bloomFilterLength in bloomFilterLengths: # 4
                print(bloomFilterLength)
                clientScript(bloomFilterLength,corruptionLevel)
                time.sleep(30)

for corruptionLevel in corruptionLevels:
    for orderingFunction in sortedOrdering:
        for bloomFilterLength in bloomFilterLengths:
            for comparThresholdDynamic in comparThresholdDynamics:
                for staticLinkageSimilarityThreshold in staticLinkageSimilarityThresholds:             
                    tempAveragePrityPercentage,tempPerfPurityPercentage = (0,0)#runExperiment(corruptionLevel,orderingFunction,bloomFilterLength,staticLinkageSimilarityThreshold,comparThresholdDynamic)
                    
                    if(tempAveragePrityPercentage>bestAveragePrityPercentage):
                        bestAveragePrityPercentage = tempAveragePrityPercentage
                        bestPerfPurityPercentage = tempPerfPurityPercentage

                        bestCorruptionLevel = corruptionLevel
                        bestOrderingFunction = orderingFunction
                        bestBloomFIlterLEngth = bloomFilterLength
                        bestSimilarityThresholdDynamic = comparThresholdDynamic
                        bestStaticLinkageSimilarityThreshold = staticLinkageSimilarityThreshold

print("---SCORES---")
print(f"bestAveragePrityPercentage: {bestAveragePrityPercentage}\nbestPerfPurityPercentage: {bestPerfPurityPercentage}")
print("---PARAMETERS---")
print(f"\nbestCorruptionLevel: {bestCorruptionLevel}\nbestOrderingFunction: {bestOrderingFunction}\nbestBloomFIlterLength: {bestBloomFIlterLEngth}\nbestSimilarityThresholdDynamic: {bestSimilarityThresholdDynamic}\nbestStaticLinkageSimilarityThreshold: {bestStaticLinkageSimilarityThreshold}")