import sys, os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
import time
from Server_program.server import Server

from Client_program.Modules.FileEncoder import FileEncoder
from Client_program.ClientEncoder import ClientEncoder
import subprocess
import tempfile

def makeNewServer(sorted, simthresh,compthresh):
    port=43555
    maxConnections=15
    server = Server(maxConnections, sortedOrdering = sorted, similarityThreshold=simthresh, comparisonThreshold=compthresh)
    server.setUpSocketOnCurrentMachine(port)
    results = server.launchServer()
    server.shutdown
    return results


def fileLocation(corruption, number):
    locationString = "./Client_program/datasets_synthetic/ncvr_numrec_500_modrec_2_ocp_" + str(corruption) + "_myp_" + str(number) + "_nump_5.csv"
    return locationString


def runExperiment(corruption,ordered,bflen,statThresh,dynThresh):
    result = makeNewServer(ordered,statThresh,dynThresh)
    time.sleep(2)
    return result
    

#runExperiment(0,True,50,0.75,0.8)



# grid search optimising average purity percentage for each curruption level so that we can use that data for analysis of our system
corruptionLevels = [20] # 3
sortedOrdering = [True]#, False] # Boolean ordered = True | False
bloomFilterLengths = [20, 50, 80, 110] # 3
comparThresholdDynamics = [0.4,0.5,0.6,0.7,0.8,0.9] #
staticLinkageSimilarityThresholds = [0.7,0.8,0.9]

bestCorruptionLevel = corruptionLevels[0]
bestOrderingFunction = sortedOrdering[0]
bestBloomFIlterLEngth = bloomFilterLengths[0]
bestSimilarityThresholdDynamic = comparThresholdDynamics[0]
bestStaticLinkageSimilarityThreshold = staticLinkageSimilarityThresholds[0]

for corruptionLevel in corruptionLevels: # 432
    bestAveragePrityPercentage = 0
    bestPerfPurityPercentage = 0
    print(corruptionLevel)
    for orderingFunction in sortedOrdering: # 144
        for bloomFilterLength in bloomFilterLengths: # 72
            print(bloomFilterLength)
            for comparThresholdDynamic in comparThresholdDynamics: # 18
                print(comparThresholdDynamic)
                for staticLinkageSimilarityThreshold in staticLinkageSimilarityThresholds:   # 3
                    print(staticLinkageSimilarityThreshold)          
                    tempAveragePrityPercentage,tempPerfPurityPercentage = runExperiment(corruptionLevel,orderingFunction,bloomFilterLength,staticLinkageSimilarityThreshold,comparThresholdDynamic)
                    #print(tempAveragePrityPercentage)
                    #print(tempPerfPurityPercentage)
                    
                    if(tempAveragePrityPercentage>bestAveragePrityPercentage):
                        bestAveragePrityPercentage = tempAveragePrityPercentage
                        bestPerfPurityPercentage = tempPerfPurityPercentage

                        bestCorruptionLevel = corruptionLevel
                        bestOrderingFunction = orderingFunction
                        bestBloomFIlterLEngth = bloomFilterLength
                        bestSimilarityThresholdDynamic = comparThresholdDynamic
                        bestStaticLinkageSimilarityThreshold = staticLinkageSimilarityThreshold
    print("-------------")
    print(f"BEST PARAMETERS AND THEIR SCORES FOR {corruptionLevel}% CORRUPTION LEVEL")
    print("\nSCORES")
    print(f"bestAveragePrityPercentage: {bestAveragePrityPercentage}\nbestPerfPurityPercentage: {bestPerfPurityPercentage}")
    print("\nPARAMETERS")
    print(f"SortedOrderingFunction: {bestOrderingFunction}\nbestBloomFilterLength: {bestBloomFIlterLEngth}\nbestSimilarityThresholdDynamic: {bestSimilarityThresholdDynamic}\nbestStaticLinkageSimilarityThreshold: {bestStaticLinkageSimilarityThreshold}")
    print("-------------")


"""
Redundant functions where we attempted to use multiprocessing/ threading to 
def clientScript(bfLen,corruption):
    staticCount=3
    total=5
    encoders = ClientEncoder(staticCount,total,corruption=corruption,bfLen=bfLen)
    encoders.runAllClients()

    programCall = "python -u ./Client_program/Modules/computeMetrics.py"
    time.sleep(30)
    proc = subprocess.Popen(programCall)

def serverScript(ordered,statThresh,dynThresh):   
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
    
"""