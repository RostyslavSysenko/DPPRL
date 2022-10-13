import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from data_structures.ClusterList import *
from data_structures.Indixer import *

# -----------------TESTING------------------------
# tests to be ran 1 section at a time with other sections
# to be commented out (for example 1.1 and 1.2 belong to the same section 1)
# Also some tests are automated and others are not and 

# TEST SET 1: some tests on mean vectors (Ross)

# # TEST SET 1.1: cluster class and static insertion, mean vector aggr (passed on 20 sep and before)
# cList = ClusterList()

# nonEncodedDict = dict()
# nonEncodedDict["name"] = "John"

# c0 = Cluster() # the true bit string is 1101
# c0.addOneRowToCluster(Row(encodedStr="1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1)) 
# c0.addOneRowToCluster(Row("1100",nonEncodedAttrubuteDict=nonEncodedDict,rowId=2,DbId=1))
# c0.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=3,DbId=1))
# c0.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=4,DbId=1))

# print(c0)

# c1 = Cluster() # the true bit string is 1111
# c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=2))
# c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=3))
# c1.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=4))
# c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=5))

# print(c1)

# c2 = Cluster() # the true bit string is 0011
# c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
# c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
# c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
# c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))

# cList.addClusterStaticly(c0)

# print(cList)

# cList.addClusterStaticly(c1)

# print(cList)

# cList.addClusterStaticly(c2)

# print(cList)

# #TEST SET 1.2: cluster class and dynamic insertion, mean vector aggr

# rowForDynamicInsertion = Row("1111")
# cList.addRowDynamic(rowForDynamicInsertion)

# print(cList)

# rowForDynamicInsertion = Row("0011")
# cList.addRowDynamic(rowForDynamicInsertion)

# print(cList)

# # All tests in TEST1 are behaving apropriately on current version of code (pushed on 20 sep 6:07pm)











# # TEST SET 2 - same as test 1, just using the median vector (Ross)

# TEST SET 2.1 cluster class and static insertion, median vector aggr
# cList = ClusterList(clusterAggrFunction= AggrFunct.MEDIAN)

# c0 = Cluster() # the true bit string is 1101
# c0.addOneRowToCluster(Row("1101")) 
# c0.addOneRowToCluster(Row("1100"))
# c0.addOneRowToCluster(Row("1101"))
# c0.addOneRowToCluster(Row("1101"))

# print(c0)

# c1 = Cluster() # the true bit string is 1111
# c1.addOneRowToCluster(Row("1111"))
# c1.addOneRowToCluster(Row("1111"))
# c1.addOneRowToCluster(Row("1101"))
# c1.addOneRowToCluster(Row("1111"))

# print(c1)

# c2 = Cluster() # the true bit string is 0011
# c2.addOneRowToCluster(Row("0011"))
# c2.addOneRowToCluster(Row("0011"))
# c2.addOneRowToCluster(Row("0011"))
# c2.addOneRowToCluster(Row("0011"))

# cList.addClusterStaticly(c0)

# print(cList)

# cList.addClusterStaticly(c1)

# print(cList)

# cList.addClusterStaticly(c2)

# print(cList)

# # # # TEST SET 2.2: cluster class and dynamic insertion, median vector aggr

# rowForDynamicInsertion = Row("1111")
# cList.addRowDynamic(rowForDynamicInsertion)

# print(cList)

# rowForDynamicInsertion = Row("0011")
# cList.addRowDynamic(rowForDynamicInsertion)

# print(cList)

# # # # All tests in TEST2 are behaving apropriately on current version of code (updated on 20 sep 6pm)

 







## TEST SET 3 - incremental linkage
###### Initial incremental linkage tests 

# a = ['11001', '11011', '11110']
# b = ['11001', '11011', '11110']
# c = ['11011', '10001', '11110']

# print(staticLinkage(a,b,c))









# # TEST SET 4 - testing Row JSON parsing

# communicatedStr1=  """
# {
#             "encodedAttributes" : 
#                 {
#                     "DOB" : "11",
#                     "wealth" : "10"
#                 },
#             "nonEncodedAttributes" : 
#                 {
#                     "weight" : 
#                         {
#                             "value" : "67" ,
#                             "type"  : "4"
#                         },
#                     "height" : 
#                         {
#                             "value" : "97" ,
#                             "type"  : "3" 
#                         }
#                 },
#             "rowId" : "1",
#             "DBId" : "3"
# }
# """

# row = Row.parseFromJson(communicatedStr1)

# print(row)

# All tests in TEST4 are behaving apropriately on current version of code on 20sep 6:30pm











# # TEST SET 5 + guide for Indexing (building initial index, getting relevant rows based on the index) (Ross). Also here we start using automated tests (all passed checked 13oct 1:30pm)

# # each row contains 3 attributes where each attribute is encoded using 4 bits
# rowLst = []
# row1 =Row("110100001010")
# rowLst.append(row1)
# row2 = Row("000011111010")
# rowLst.append(row2)
# row3 = Row("000001001010")
# rowLst.append(row3)
# row4 = Row("111110101010")
# rowLst.append(row4)

# # only 2 attributes out of 3 will be used for multi stage indexing
# ListOfAttribute_OrderTupples = list()
# ListOfAttribute_OrderTupples.append(("zipCode",0))
# ListOfAttribute_OrderTupples.append(("City",1))

# #here we create indexer and test its functionality

# indixer = Indexer(bitsPerAttribute = 4, ListOfAttribute_OrderTupples = ListOfAttribute_OrderTupples)

# indixer.initialIndexBuild(rowList=rowLst)

# comparisonAttributeFunction = lambda row: row.encodedRowString

# # TEST 5.1 (automated)
# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001011"))
# lst_test = [row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)

# # TEST 5.2 (automated)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("000011110000"))
# lst_test = [row2,row3] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)









# # TEST 6 checking whether the indexers are updated apropriately when new rows are inserted (automated test)

# # each row contains 3 attributes where each attribute is encoded using 4 bits
# rowLst = []
# row1 =Row("110100001010")
# rowLst.append(row1)
# row2 = Row("000011111010")
# rowLst.append(row2)
# row3 = Row("000001001010")
# rowLst.append(row3)
# row4 = Row("111110101010")
# rowLst.append(row4)

# # only 2 attributes out of 3 will be used for multi stage indexing
# ListOfAttribute_OrderTupples = list()
# ListOfAttribute_OrderTupples.append(("zipCode",0))
# ListOfAttribute_OrderTupples.append(("City",1))

# #here we create indexer and test its functionality

# indixer = Indexer(bitsPerAttribute = 4, ListOfAttribute_OrderTupples = ListOfAttribute_OrderTupples)

# indixer.initialIndexBuild(rowList=rowLst)

# comparisonAttributeFunction = lambda row: row.encodedRowString


# # TEST 6.1 (automated)
# insertRow1 = Row("111100000000")
# indixer.updateIndexingDictOnInsert(insertedRow=insertRow1)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001111"))
# lst_test = [insertRow1,row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)



# # TEST 6.2 (automated)
# insertRow2 = Row("101010101010")
# indixer.updateIndexingDictOnInsert(insertedRow=insertRow2)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001111"))
# lst_test = [insertRow1,row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)



# # TEST 6.3 (automated)
# insertRow3 = Row("101010101111")
# indixer.updateIndexingDictOnInsert(insertedRow=insertRow3)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001111"))
# lst_test = [insertRow1,row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)