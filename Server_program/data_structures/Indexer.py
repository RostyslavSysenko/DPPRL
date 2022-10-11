from enum import Enum
import statistics
import json


class Indexer:


    def __init__(self,indexingBitStart=None, indexingBitEnd = None):
        self.indexingDictionary = dict() # used for indexing
        self.indexingBitStart = indexingBitStart
        self.indexingBitEnd = indexingBitEnd
    
    def indexingHasNotBeenDoneYet(self):
        return len(self.indexingDictionary) == 0


class Row:
    # non modifiable currently
    def __init__(self,encodedStr: str, nonEncodedAttrubuteDict =None, rowId = None, DbId = None):
        self.encodedRowString = encodedStr
        self.rowListRepresentation = [int(char) for char in encodedStr]
        self.nonEncodedAttrubuteDict =nonEncodedAttrubuteDict

        self.rowId =rowId
        self.DbId=DbId

        self.clusterRef = None # this will be updated during cluster assignment


        def parseFromJson(jsonStr):
    # parse jsonStr into dictionary object:
            jsonObj = json.loads(jsonStr)

        # creating encoded string
            lstOfEncodings = list(jsonObj["encodedAttributes"].values())
            encodedStr =   ''.join(lstOfEncodings) #concat all encodings in a list


            row = Row(
                DbId= jsonObj["DBId"],
                rowId = jsonObj["rowId"],
                encodedStr = encodedStr,
                nonEncodedAttrubuteDict= jsonObj["nonEncodedAttributes"]
                )
            return row

    
    def initialIndexBuild(self, Row): # [Row(),Row()..]
        # input: list of Row objects 
        # out: build up self.indexingDictionary

        row_build = {self.DbId,self.rowId}


        values = row_build.values
        values_list = list(values)


        value = values_list[0]


        print (value)

      

        # list 

        #index = index.encodedStr[3:100]
        #index = index.nonEncodedAttrubuteDict dictionati["name"] -> "josh"
        
        # TO-DO
        # build the indexing into the self.indexingDictionary
        
    
    def getIndexingKey(self,Row):
        # INPUT : row object
        # outout: some sort of key (maybe string or number)
        # TO-DO
        # takes in a row and based on the indexing specification of ClusterList extracts the indexing key and returns it

        row_build = {self.DbId,self.rowId}

        keys_list  = list(row_build)
        
        key = keys_list[0]

        print(key)





        





        #search_key = '0101'

        #res = list(encodedStr.keys()).index(search_key) #cant figure this one out, but very similar to this

        #print(str(res))





        

        # step 2:
        # def updateIndexingDict():
        #     # when row is inserted with indexing turned on, the index should update after insertion
        #     pass

        # step2: def multistage indexing 



indexerObject = Indexer()

#indexerObject.initialIndexBuild(listRows)

# row encoding = "0101 0010 0101" and we want the key of that encoding to be first 4 bits
# suppose we choose first 4 bits for indexing then indexing key = "0101"

# indexerObject.indexingDictionary[indexingKey] -> relevant staff (relevant rows)

