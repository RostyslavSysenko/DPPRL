from array import *
import statistics
from sklearn.neighbors import NearestNeighbors
import json

class ClusterList:
    def __init__(self, cosineSimilarityThreshold = 0.9,clusterAggrFunction = "mean",indexingBitStart=None, indexingBitEnd = None ):
        self.nextAvailIndex = 0
        self.cosineSimilarityThreshold = cosineSimilarityThreshold
        self.clusterAggrFunction =clusterAggrFunction
        self.clusterList = []
        self.clusterAggregations = []; # 2d array of clusters and each cluster array contains 0/1 bit encodings
        
        self.indexingDictionary = dict()
        self.indexingBitStart = indexingBitStart
        self.indexingBitEnd = indexingBitEnd

    def __addNewClusterToClusterList(self,clusterObj):
        # insertion
        clusterObj.updateClusterOnClusterListInsertion(self,self.nextAvailIndex)
        self.nextAvailIndex = self.nextAvailIndex+1
        self.clusterAggregations.append(clusterObj.getClusterListRepresentation())
        self.clusterList.append(clusterObj)

    def indexingHasNotBeenDoneYet(self):
        return len(self.indexingDictionary)==0 

    def __growExistingClusterInAClusterList(self,row, clusterIdxToWhichWeAdd):
        self.clusterList[clusterIdxToWhichWeAdd].addOneRowToCluster(row) #CLUSTER gets updated
        self.clusterAggregations[clusterIdxToWhichWeAdd] = self.clusterList[clusterIdxToWhichWeAdd].getClusterListRepresentation()

    def addClusterStaticly(self,clusterObj):
        # assign and increment index
        self.__addNewClusterToClusterList(clusterObj)

    def addRowDynamicNaive(self, row, indexingTurnedOn=False,indexingKey =None):
        # this is a naive implimentation of dynamic linkage which refits the model every time a dynamic linkage is needed and then finds 1 NN based on that newly created model
        # we assume the order of clusers never changes (meaning clusters are never deleted or reordered)
        knn_classifier = NearestNeighbors(n_neighbors=1, metric="cosine")
        if (not indexingTurnedOn):
            knn_classifier.fit(self.clusterAggregations) # fit the model based on the whole data
        else:
            indexedClusterAggregations = self.indexingDictionary[indexingKey]
            knn_classifier.fit(indexedClusterAggregations) #fit the model based on subset of data
        
        distance_mat, neighbours_vec = knn_classifier.kneighbors([row.rowListRepresentation])
        clusterIdx= neighbours_vec[0][0] # gets us index of cluster that we want to modify
        cosineSimilarity = 1 - distance_mat[0][0]
        #print("cos sim: "+str(cosineSimilarity) + " & reccomended neighbout is at idx: " + str(clusterIdx))

        if (cosineSimilarity >= self.cosineSimilarityThreshold): # cosine similarity is high 
            self.__growExistingClusterInAClusterList(row, clusterIdx)
        else: # cosine similarity is low 
            new_cluster = Cluster()
            new_cluster.addOneRowToCluster(row)
            self.__addNewClusterToClusterList(new_cluster)

        if indexingTurnedOn:
            self.updateIndexingDict()
    
    def initialIndexBuild(self):
        # TO-DO
        # build the indexing into the self.indexingDictionary
        pass
    
    def getIndexingKey(self,row):
        # TO-DO
        # takes in a row and based on the indexing specification of ClusterList extracts the indexing key and returns it
        pass

    def updateIndexingDict():
        # when row is inserted with indexing turned on, the index should update after insertion
        pass

    def addRowDynamicAdv1(self,row,indexingKey):
        # sets up indexing dictionary, then on insertion fits knn model to the set of clusters corresponding to the index and makes prediction
        if(self.indexingHasNotBeenDoneYet()):
            self.initialIndexBuild()
        
        self.addRowDynamicNaive(row,indexing=True, indexingKey = indexingKey)
    
    def __str__(self) -> str:
        returnedStr = "\n" + "largestOccupiedIndex : " + str(self.nextAvailIndex-1) +  "\n" + "cluster aggr function: " + str(self.clusterAggrFunction) + "\n" +"clusterReps: " + str(self.clusterAggregations) +"\n"+"numberOfItemsInEachCluster: ["

        for cluster in self.clusterList:
            returnedStr = returnedStr + str(cluster.getNumberOfStoredRows()) + ", "

        returnedStr = returnedStr + "]"
        return returnedStr
    

class Cluster:
    def __init__(self,id = None,clusterAggFunction = None):
        self.__clusterId = id
        self.__parentClusterListObj = None

        self.__clusterRowObjLst = []
        self.__clusterVecAggr = []

    def __clusterDoesntBelongToClustList(self):
        return self.__parentClusterListObj == None

    def getNumberOfStoredRows(self):
        return len(self.__clusterRowObjLst)

    def __getAggrFunction(self):
        if (self.__clusterDoesntBelongToClustList()):
            return "mean" # this is default when we create cluster without them belonging to cluster list. This is used for testing
        else:
            return self.__parentClusterListObj.clusterAggrFunction

    def __getRowNum(self):
        return len(self.__clusterRowObjLst)
    
    def __getAttributeNum(self):
        return len(self.__clusterRowObjLst[0].rowListRepresentation)

    def __setClusterAggrToMeanVector(self):
        #assume cluster has at least 1 row
        assert len(self.__clusterRowObjLst)>0

        meanVector = []
        rowsNum = self.__getRowNum()
        colsNum = self.__getAttributeNum()
        
        for j in range(0,colsNum):
            sum = 0
            n = 0

            for i in range(0,rowsNum):
                sum = sum + self.__clusterRowObjLst[i].rowListRepresentation[j]
                n = n+1
            
            mean = sum/n
            meanVector.append(mean)
        
        self.__clusterVecAggr = meanVector

    def __setClusterAggrToMedianVector(self):
        #assume cluster has at least 1 row
        assert len(self.__clusterRowObjLst)>0

        medianVector = []
        
        for j in range(0,self.__getAttributeNum()):
            colVector = []
            for i in range(0,self.__getRowNum()):
                colVector.append(self.__clusterRowObjLst[i].rowListRepresentation[j])

            median = statistics.median(colVector)
            medianVector.append(median)
        
        self.__clusterVecAggr = medianVector

    def getClusterListRepresentation(self):
        return self.__clusterVecAggr

    def updateClusterOnClusterListInsertion(self,parentClusterListObjRef, clusterListClusterIdx):
        self.__parentClusterListObj = parentClusterListObjRef
        self.__clusterId = clusterListClusterIdx

        self.__handleAggregation()

    def getId(self):
        return self.__clusterId

    def addOneRowToCluster(self, row):
        self.__clusterRowObjLst.append(row) # updating the row list
        # updating the cluster representation
        self.__handleAggregation()

    def __handleAggregation(self):
        if (self.__getAggrFunction() == "mean"):
            self.__setClusterAggrToMeanVector()
        elif (self.__getAggrFunction() == "median"):
            self.__setClusterAggrToMedianVector()
        else:
            assert False, "invalid aggregation function reached: '" + self.__getAggrFunction() + "'"

    def __str__(self):
        ## this method helps to display what the cluster looks like to help with debugging
        string = "\n" + "cluster id : " + str(self.__clusterId) + "\n" + "cluster row Objects : " 
        
        for row in self.__clusterRowObjLst:
            string = string + "\n" + "    - " + str(row)
            
        string  = string + "\n" + "cluster agg vec : " + str(self.__clusterVecAggr) + "\n"
        return string 

class Row:
    # non modifiable currently
    def __init__(self,encodedStr: str, nonEncodedAttrubuteDict =None, rowId = None, DbId = None):
        self.encodedRowString = encodedStr
        self.rowListRepresentation = [int(char) for char in encodedStr]
        self.nonEncodedAttrubuteDict =nonEncodedAttrubuteDict
        self.rowId =rowId
        self.DbId=DbId
    
    def parseFromJson(jsonStr):
        """
        input: a string of type 

        '
        {

            "encodedAttributes" : 
                {
                    "DOB" : "01000101010100111",
                    "encName2" : ...
                    ... 
                    "encNamek" : ...
                },
            "nonEncodedAttributes" : 
                {
                    "weight" : 
                        {
                            "value" : "67" 
                            "type"  : "4" #val is based on the Enum we defined
                        },
                    "attName2" : ...
                    ...
                    "attNamej" : ...
                },
            "rowId" : "q",
            "DBId" : "z"

        }
        '
        output: parsedRow Object
        """

        # parse jsonStr into dictionary object:
        jsonObj = json.loads(jsonStr)

        # creating encoded string
        lstOfEncodings = list(jsonObj["encodedAttributes"].values())
        encodedStr =   ''.join(lstOfEncodings) #concat all encodings in a list

        # creating a row from python dictionary:
        row = Row(
                DbId= jsonObj["DBId"],
                rowId = jsonObj["rowId"],
                encodedStr = encodedStr,
                nonEncodedAttrubuteDict= jsonObj["nonEncodedAttributes"]
                )
        return row

    def __str__(self):
        sep = "---Row---" + "\n"
        idStr = "id: " + self.rowId + "\n"
        dbStr = "db: " + self.DbId + "\n"
        encStr = "enc Attrs: " + self.encodedRowString + "\n"
        nonEncStr = "nonEnc Attrs: " + str(self.nonEncodedAttrubuteDict) + "\n"
        return sep + idStr + dbStr + encStr + nonEncStr

