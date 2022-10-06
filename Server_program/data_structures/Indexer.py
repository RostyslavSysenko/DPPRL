class Indexer:


    def __init__(self,indexingBitStart=None, indexingBitEnd = None):
        self.indexingDictionary = dict() # used for indexing
        self.indexingBitStart = indexingBitStart
        self.indexingBitEnd = indexingBitEnd
    
    def indexingHasNotBeenDoneYet(self):
        return len(self.indexingDictionary) == 0

    def initialIndexBuild(self, rowList): # [Row(),Row()..]
        # input: list of Row objects 
        # out: build up self.indexingDictionary 

        index = index.encodedStr[3:20]

        print(index) #need to add more in the indexing to connect it to the indexing 



        #or 

        
        encodedStr_at_index = list(dic.encodedStr())[index]

        # list 

        #index = index.encodedStr[3:100]
        #index = index.nonEncodedAttrubuteDict dictionati["name"] -> "josh"
        
        # TO-DO
        # build the indexing into the self.indexingDictionary
        pass
    
    def getIndexingKey(self,row):
        # INPUT : row object
        # outout: some sort of key (maybe string or number)
        # TO-DO
        # takes in a row and based on the indexing specification of ClusterList extracts the indexing key and returns it

        search_key = '0101'

        res = list(encodedStr.keys()).index(search_key) #cant figure this one out, but very similar to this

        print(str(res))





        pass

        # step 2:
        # def updateIndexingDict():
        #     # when row is inserted with indexing turned on, the index should update after insertion
        #     pass

        # step2: def multistage indexing 



indexerObject = Indexer()

indexerObject.initialIndexBuild(listRows)

# row encoding = "0101 0010 0101" and we want the key of that encoding to be first 4 bits
# suppose we choose first 4 bits for indexing then indexing key = "0101"

# indexerObject.indexingDictionary[indexingKey] -> relevant staff (relevant rows)

