from Clustering import *
from staticLinkage import staticLinkage 
# -----------------TESTING------------------------

# # TEST SET 1: some tests on mean vectors

# # TEST SET 1.1: cluster class and static insertion, mean vector aggr
# cList = ClusterList()

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

# # TEST SET 1.2: cluster class and dynamic insertion, mean vector aggr

# rowForDynamicInsertion = Row("1111")
# cList.addRowDynamicNaive(rowForDynamicInsertion)

# print(cList)

# rowForDynamicInsertion = Row("0011")
# cList.addRowDynamicNaive(rowForDynamicInsertion)

# print(cList)

# # All tests in TEST1 are behaving apropriately on current version of code






# # TEST SET 2 - same as test 1, just using the median vector

# TEST SET 2.1 cluster class and static insertion, median vector aggr
# cList = ClusterList(clusterAggrFunction= "median")

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

# # # TEST SET 2.2: cluster class and dynamic insertion, median vector aggr

# rowForDynamicInsertion = Row("1111")
# cList.addRowDynamicNaive(rowForDynamicInsertion)

# print(cList)

# rowForDynamicInsertion = Row("0011")
# cList.addRowDynamicNaive(rowForDynamicInsertion)

# print(cList)

# # # # All tests in TEST2 are behaving apropriately on current version of code


###### Initial incremental linkage tests 

# a = ['11001', '11011', '11110']
# b = ['11001', '11011', '11110']
# c = ['11011', '10001', '11110']

# print(staticLinkage(a,b,c))