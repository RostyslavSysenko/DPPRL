class Indexer:
    """
    this class is used to help with speed of clustering, by blocking out rows/cluster that we dont believe are relevant

    assumptions: we assume that each attribute takes exact same number of blume filter bits

    inputs: number of bits allocated for each attribute and a list of attributeName-order tupples. For example, look into the testing doc 
    for data structures
    """
    def __init__(self,bitsPerAttribute, ListOfAttribute_OrderTupples):
        # INPUTS:
            # ListOfAttribute_OrderTupples WILL look like this [(orderNum_1, AttriName_1),(orderNum_2, AttriName_2),...,(orderNum_n, AttriName_n)]
            # the orderNum_i depends on the encoding of the row. So if we have a row encoding as follows 000011110101 and each attribute was taking 4 bits
            # and 0000 was encoding for zipcode and 1111 was encoding for age and 0101 represnts cityName, then our attribute order tupple would look as follows:
                # [(0,"zipcode"),(1, "age")]
                # for this to work we must have each attribute taking same number of bits
                #  note cityName attribute is not indexed over since it is not included in attribute order tupple, but if we wantted to index based on that too, then we would have to include it
            # list of order tupples doesnt have to include all attributes, but instead just includes attributes over which we want to index
        self.listOfInxedDictionaries = []
        self.listofIndexedAttributeNames = []

        self.attributeDict = dict() # maps attributeName -> attribtuePosition (starting from 0)
        
        #filling up attributeDict
        for attributeOrderTupple in ListOfAttribute_OrderTupples:
            attributeName,orderInt = attributeOrderTupple
            self.attributeDict[attributeName] = orderInt

        self.bitPerAttribute = bitsPerAttribute # assume all attributes have same length encoding
    
    def getPositionOfattributesFirstDigitWithinEncodedStr(self, attributeName):
        # finds the starting position of substring corresponding to encoded attribute attributeName across all row.encodedstring
        relativeOrderCountOfAttribute = self.attributeDict[attributeName]
        return self.bitPerAttribute*relativeOrderCountOfAttribute
    
    def getPositionOfattributesLastDigitWithinEncodedStr(self, attributeName):
        # finds the ending position of substring corresponding to encoded attribute attributeName across all row.encodedstring
        relativeOrderCountOfAttribute = self.attributeDict[attributeName]
        return self.bitPerAttribute*(relativeOrderCountOfAttribute+1)

    def getIndexingKey(self,row,attributeName):
        # gets getEncodedAttributeValueForRow

        idxStart = self.getPositionOfattributesFirstDigitWithinEncodedStr(attributeName)
        idxEnd = self.getPositionOfattributesLastDigitWithinEncodedStr(attributeName)
        return row.encodedRowString[idxStart:idxEnd]

    def indexingHasNotBeenDoneYet(self):
        return len(self.listOfInxedDictionaries) == 0 # there are 0 indexing dictionaries that we have built so far

    def initialIndexBuild(self,rowList):
        # out: nothing gets returned since the fucntion just updates the data structure
        # build the indexing into the self.indexingDictionary
        for attributeName in self.attributeDict.keys():
            indexer = dict()

            for row in rowList:
                rowIndex = self.getIndexingKey(row = row,attributeName = attributeName)
                if rowIndex not in indexer.keys():
                    indexer[rowIndex]= list()
                indexer[rowIndex].append(row)
            
            self.listOfInxedDictionaries.append(indexer)
            self.listofIndexedAttributeNames.append(attributeName)

    def getRowsWithAtLeast1SameKey(self,row):
        # gets a set of rows that have at least 1 same indexing key as the row
        
        allRows = list()
        
        for i in range(0, len(self.listOfInxedDictionaries)):
            idxDict = self.listOfInxedDictionaries[i]
            attrName = self.listofIndexedAttributeNames[i] # attribute corresponding to currentIndexDictionary

            
            relevantKey = self.getIndexingKey(row,attrName)
            if relevantKey in idxDict.keys(): #only concider adding more rows to the returned set if an index already exists for the relevant keys
                rowListCurr = idxDict[relevantKey]

                setAllRows = set(allRows)
                setRowCurr = set(rowListCurr)

                union = setAllRows.union(setRowCurr)
                allRows = list(union)
        return allRows

    def getClustersWithAtLeast1RowWithSameKey(self, row):
        rowList = self.getRowsWithAtLeast1SameKey(row)

        clusterSet = set()

        for row in rowList:
            cluster = row.clusterRef 
            clusterSet.add(cluster)
        
        return list(clusterSet)

    def updateIndexingDictOnInsert(self,insertedRow):
        # pre-condition: assumes that indexing dictionaries had already been built
        # out: nothing gets returned since the fucntion just updates the data structure
        # build the indexing into the self.indexingDictionary

        # for all indexing dictionaries 
        for i in range(0,len(self.listOfInxedDictionaries)):
            
            # get the indexing dictionary
            indexer = self.listOfInxedDictionaries[i]

            # get the attribute which the current indexing dictionary captures
            attributeIndexedByCurrentDict = self.listofIndexedAttributeNames[i]

            # get the key of the inserted row corresponding to the attribute of the currently concidered indexing dictionary
            rowIndex = self.getIndexingKey(row = insertedRow,attributeName = attributeIndexedByCurrentDict)
            
            # grow the indexing dictionary
            if rowIndex not in indexer.keys():
                indexer[rowIndex]= list()
            indexer[rowIndex].append(insertedRow)
            

            