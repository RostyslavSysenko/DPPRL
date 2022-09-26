class Indexer:
    def __init__(self,indexingBitStart=None, indexingBitEnd = None):
        self.indexingDictionary = dict() # used for indexing
        self.indexingBitStart = indexingBitStart
        self.indexingBitEnd = indexingBitEnd
    
    def indexingHasNotBeenDoneYet(self):
        return len(self.indexingDictionary) == 0

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