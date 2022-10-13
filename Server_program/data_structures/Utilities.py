from enum import Enum
import statistics
import json

class AggrFunct(Enum):
    MEAN = 1
    MEDIAN = 2

class Operation(Enum):
    INSERT = 1
    DELETE = 2


class Row:
    # non modifiable currently
    def __init__(self,encodedStr: str, nonEncodedAttrubuteDict =None, rowId = None, DbId = None):
        self.encodedRowString = encodedStr # "010010101010" , we assume that attribtue encodings are concated and all are of same length
        self.rowListRepresentation = [int(char) for char in encodedStr] # [0,1,0,0,..0]
        self.nonEncodedAttrubuteDict =nonEncodedAttrubuteDict # weight -> 67, 

        self.rowId =rowId
        self.DbId=DbId

        self.clusterRef = None # this will be updated during cluster assignment
    
    def parseFromJson(jsonStr):
        """
        input: a string of type valid JSON with the following set of attributes

        '
        {

            "encodedAttributes" : 
                {
                    "DOB" : "01000101010100111", #10-20-2013
                    "encName2" : ...
                    ... 
                    "encNamek" : ...
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
        idStr = "id: " + str(self.rowId) + "\n"
        dbStr = "db: " + str(self.DbId) + "\n"
        encStr = "enc Attrs: " + str(self.encodedRowString) + "\n"
        nonEncStr = "nonEnc Attrs: " + str(self.nonEncodedAttrubuteDict) + "\n"
        return sep + idStr + dbStr + encStr + nonEncStr


class Cluster:
    def __init__(self,id = None,clusterAggFunction = None):
        self.__clusterId = id
        self.__parentClusterListObj = None

        self.__clusterRowObjLst = [] # [RowObj1,RowObj2...]
        self.__clusterVecAggr = [] # [0.04,0.5,1...]

    def __clusterDoesntBelongToClustList(self):
        return self.__parentClusterListObj == None

    def getClusterRowObjList(self):
        return self.__clusterRowObjLst

    def getNumberOfStoredRows(self):
        return len(self.__clusterRowObjLst)

    def __getAggrFunction(self):
        if (self.__clusterDoesntBelongToClustList()):
            return AggrFunct.MEAN # this is default when we create cluster without them belonging to cluster list. This is used for testing
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
        row.clusterRef = self
        self.__clusterRowObjLst.append(row) # updating the row list
        # updating the cluster representation

        self.__handleAggregation()

    def __handleAggregation(self):
        if (self.__getAggrFunction() == AggrFunct.MEAN):
            self.__setClusterAggrToMeanVector()
        elif (self.__getAggrFunction() == AggrFunct.MEDIAN):
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