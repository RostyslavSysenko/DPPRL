import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from data_structures.ClusterList import *
from data_structures.Indixer import *
from clustering.DynamicClustering import DynamicClusterer

# -----------------TESTING------------------------
# tests to be ran 1 section at a time with other sections
# to be commented out (for example 1.1 and 1.2 belong to the same section 1)
# Also some tests are automated and others are not and 

# TEST SET 1: some tests on mean vectors (Ross)

# # TEST SET 1.1: cluster class and static insertion, mean vector aggr (passed on 20 sep and before)
cList = ClusterList()

nonEncodedDict = dict()
nonEncodedDict["name"] = "John"

c0 = Cluster() # the true bit string is 1101
c0.addOneRowToCluster(Row(encodedStr="1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1)) 
c0.addOneRowToCluster(Row("1100",nonEncodedAttrubuteDict=nonEncodedDict,rowId=2,DbId=1))
c0.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=3,DbId=1))
c0.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=4,DbId=1))

print(c0)

c1 = Cluster() # the true bit string is 1111
c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=2))
c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=3))
c1.addOneRowToCluster(Row("1101",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=4))
c1.addOneRowToCluster(Row("1111",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=5))

print(c1)

c2 = Cluster() # the true bit string is 0011
c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))
c2.addOneRowToCluster(Row("0011",nonEncodedAttrubuteDict=nonEncodedDict,rowId=1,DbId=1))

cList.addClusterStaticly(c0)

print(cList)

cList.addClusterStaticly(c1)

print(cList)

cList.addClusterStaticly(c2)

print(cList)

#TEST SET 1.2: cluster class and dynamic insertion, mean vector aggr

rowForDynamicInsertion = Row("1111")
cList.addRowDynamic(rowForDynamicInsertion, DynamicClusterer()) 

#print(cList)

rowForDynamicInsertion = Row("0011")
cList.addRowDynamic(rowForDynamicInsertion, DynamicClusterer())

print(cList)

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



# # TEST 6.2 (automated) passed on 13 of october
# insertRow2 = Row("101010101010")
# indixer.updateIndexingDictOnInsert(insertedRow=insertRow2)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001111"))
# lst_test = [insertRow1,row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)



# # TEST 6.3 (automated) passed on 13 oct
# insertRow3 = Row("101010101111")
# indixer.updateIndexingDictOnInsert(insertedRow=insertRow3)

# lst_got = indixer.getRowsWithAtLeast1SameKey(Row("111100001111"))
# lst_test = [insertRow1,row4,row1] # the output we expect

# # the automated test case
# assert sorted(lst_got,key=comparisonAttributeFunction) == sorted(lst_test,key=comparisonAttributeFunction)






# # Test 7 - (automated) - checking whether a map from list or rows to list of clusters those rows belong to work apropriately

# # setting up clusters
# c0 = Cluster()
# row1=Row("111100000000")
# c0.addOneRowToCluster(row1) 

# c1 = Cluster() 
# row2 = Row("000011110000")
# c1.addOneRowToCluster(row2)

# c2 = Cluster() 
# row3 = Row("010101010000")
# c2.addOneRowToCluster(row3)

# # checking whether 

# ListOfAttribute_OrderTupples = list()
# ListOfAttribute_OrderTupples.append(("zipCode",0))
# ListOfAttribute_OrderTupples.append(("City",1))

# indixer = Indexer(bitsPerAttribute = 4, ListOfAttribute_OrderTupples = ListOfAttribute_OrderTupples)
# indixer.initialIndexBuild(rowList=[row1,row2,row3])

# comparisonAttributeFunction = lambda cluster: cluster.getClusterListRepresentation()

# # TEST 7.1
# clusterLst1 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("000000001111"))

# test1 = [c0,c1]


# # the automated test case
# assert sorted(clusterLst1,key=comparisonAttributeFunction) == sorted(test1,key=comparisonAttributeFunction)



# # TEST 7.2
# clusterLst2 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("101010101010"))

# test2 = []

# # the automated test case
# assert sorted(clusterLst2,key=comparisonAttributeFunction) == sorted(test2,key=comparisonAttributeFunction)



# # TEST 7.3 (automated) passed 13 oct 
# clusterLst3 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("010110100000"))

# test3 = [c2]

# # the automated test case
# assert sorted(clusterLst3,key=comparisonAttributeFunction) == sorted(test3,key=comparisonAttributeFunction)

# # test 7.4

# clusterLst4 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("010110100000"))

# test4 = [c2,c1]

# # the automated test case
# assert sorted(clusterLst4,key=comparisonAttributeFunction) != sorted(test4,key=comparisonAttributeFunction)

# # test 7.5

# clusterLst5 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("111110100000"))

# test5 = [c0]

# # the automated test case
# assert sorted(clusterLst5,key=comparisonAttributeFunction) == sorted(test5,key=comparisonAttributeFunction)


# # test 7.6

# clusterLst6 = indixer.getClustersWithAtLeast1RowWithSameKey(Row("111110100000"))

# test6 = [c2]

# # the automated test case
# assert sorted(clusterLst6,key=comparisonAttributeFunction) != sorted(test6,key=comparisonAttributeFunction)







# ## Test 8 (automated) - checking whether indexer is working correctly when integrated with cluster list (tests passed on 14 oct by Ross)

# ListOfAttribute_OrderTupples = list()
# ListOfAttribute_OrderTupples.append(("zipCode",0))
# ListOfAttribute_OrderTupples.append(("City",1))

# Idxer = Indexer(bitsPerAttribute= 4,ListOfAttribute_OrderTupples=ListOfAttribute_OrderTupples)
# cList_w_blocking = ClusterList(certaintyThreshold = 0.5,clusterAggrFunction = AggrFunct.MEAN,indexer = Idxer)

# c0 = Cluster() # the true bit string is 00000000
# c0.addOneRowToCluster(Row(encodedStr="00000010",rowId=1,DbId=1)) 
# c0.addOneRowToCluster(Row("00000000",rowId=2,DbId=1))

# c1 = Cluster() # the true bit string is 11111111
# c1.addOneRowToCluster(Row("11111111",rowId=1,DbId=2))
# c1.addOneRowToCluster(Row("11111111",rowId=1,DbId=3))

# c2 = Cluster() # the true bit string is 11110000
# c2.addOneRowToCluster(Row("11110000",rowId=1,DbId=1))
# c2.addOneRowToCluster(Row("11110000",rowId=1,DbId=2))

# cList_w_blocking.addClusterStaticly(c0)
# cList_w_blocking.addClusterStaticly(c1)
# cList_w_blocking.addClusterStaticly(c2)

# #TEST SET 8.1: (automated)

# # # we expect that insertion will be made into the cluster0 since it is most similar and it has common 
# # # indexing key with our added row. This test should work with any aggregation metric
# cList_w_blocking.addRowDynamic(Row("10000000"))
# assert c0.getNumberOfStoredRows()==2 and c1.getNumberOfStoredRows()==2 and c2.getNumberOfStoredRows()==3, "Err1. cluster state is as follows: " + str(cList_w_blocking)

# #TEST SET 8.2: (automated)
# cList_w_blocking.addRowDynamic(Row("11111111"))
# # cossim(1,1,1,1,1,1,1,1 and 1,1,1,1,1,1,1,1)=1 -> winner
# # cossim(1,1,1,1,1,1,1,1 and 1.0, 0.67, 0.67, 0.67, 0.0, 0.0, 0.0, 0.0)= 3.01/sqrt(8*2.35)=0.69
# # the other cluster is not a winner
# assert c0.getNumberOfStoredRows()==2 and c1.getNumberOfStoredRows()==3 and c2.getNumberOfStoredRows()==3, "Err2. cluster state is as follows: " + str(cList_w_blocking)

# #TEST SET 8.3: (automated)
# cList_w_blocking.addRowDynamic(Row("11110000"))
# # cossim(1,1,1,1,0,0,0,0 and 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0) = 0/sqrt(2)=0
# # cossim(1,1,1,1,0,0,0,0 and .0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0) = 3/sqrt(4*7)=0.57
# # cossim(1,1,1,1,0,0,0,0 and 1.0, 0.67, 0.67, 0.67, 0.0, 0.0, 0.0, 0.0) = 2.8/sqrt(4*2.35)=0.913
# assert c0.getNumberOfStoredRows()==2 and c1.getNumberOfStoredRows()==3 and c2.getNumberOfStoredRows()==4, "Err2. cluster state is as follows: " + str(cList_w_blocking)

