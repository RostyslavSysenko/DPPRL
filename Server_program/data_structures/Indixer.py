class Indexer:
    def __init__(self,bitsPerAttribute, ListOfAttribute_OrderTupples):
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
        return len(self.indexingDictionary) == 0

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
            

            