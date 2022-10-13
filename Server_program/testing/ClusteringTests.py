# import os, sys
# parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(parentdir)
# from data_structures.Utilities import *
# from data_structures.ClusterList import *

# -----------------TESTING------------------------

# TEST SET 1: some tests on mean vectors

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






# # TEST SET 2 - same as test 1, just using the median vector

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