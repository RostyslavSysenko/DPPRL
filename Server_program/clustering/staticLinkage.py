import networkx as nx
import random
import numpy as np
import sys, os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from communication.metrics import *
from data_structures.Indixer import Indexer
import json


class staticLinker:
    def __init__(self, simThreshold=0.75, indexer=None, metricsIn=None):
        self.min_similarity_threshold = simThreshold
        self.G = nx.Graph()
        self.listOfClusters = []
        self.clusterId = 0
        self.indexer = indexer
        self.metric = metricsIn

    def random_order(self, BF_list): 
        
        result = list(BF_list)
        random.shuffle(result)

        return result

    def sorted_order(self, BF_list): 

        result = sorted(BF_list, key = len, reverse = True)

        return result

    def sim(self, a, b):
        # Debugging
        #print("Length of a and b: ", len(a), ", ", len(b))

        #common bit positions set to 1 
        z = 0 
        p = 2
        
        pos_counter = []
        a_positions = []
        b_positions = []
        
        for i in range(len(a)):
            pos_counter.append(i)
            if a[i] == '1': 
                a_positions.append(pos_counter[i])
        
        pos_counter = []
        for i in range(len(b)):
            pos_counter.append(i)
            if b[i] == '1': 
                b_positions.append(pos_counter[i])
        
        common_pos = list(set(a_positions)&set(b_positions))
        common_count = len(common_pos)
        
        z = common_count
        
        #bit positions set to 1 
        l = 0 
        
        l_a = a.count('1')
        l_b = b.count('1')
        
        if l_a > l_b:
            l = l_a 
        elif l_a < l_b: 
            l = l_b
        else: 
            l = l_a 

        
        if z == 0:
            sim=0
        else: 
            sim = p * z / (l+z)
        
        return sim


    def staticLinkage(self, DBs): 
        # input 
        # D --> Party 𝑃𝑖’s BFs
        num_of_parties = len(DBs)
        if num_of_parties != 3:
            print("ERROR Static linkage requires 3 inputs, returning empty list")
            return []

        # sim --> Similarity function

        # ord --> Ordering function for incremental processing of databases : 

        # map --> one to one mapping algo

        # min_similarity_threshold (st) --> Minimum similarity threshold to classify record sets
        min_similarity_threshold = 0.75
        # min_subset_size (sm) --> Minimum subset size, with 2 ≤ 𝑠𝑚 ≤ 𝑝
        min_subset_size = 2

        # output
        # M - matching clusters
        #intialisation 
        clus_ID = 0
        resultGraph = nx.Graph()
        for db in DBs:
            self.initaliseVertices(db,resultGraph)

        #result = []

        # order databases 
        # choose between random_order or sorted_order 
        # sorted_order is more efficient
        DBs = self.random_order(DBs)
       
       # Needs explanation here
        for i in range(num_of_parties-1):
            tempGraph = nx.Graph()
            Graph_verts = self.initaliseVertices(DBs[i], tempGraph)

            print("length of graph ", len(Graph_verts))
            # for DB in index > i 
            for Db in DBs:
                if DBs.index(Db) <= i:
                    continue

                print("length of current Db: ",len(Db))
                counting = 0

                indexerExist = False
                if self.indexer != None:
                    assert type(self.indexer) == Indexer
                    self.indexer.initialIndexBuild(Db)
                    indexerExist = True

                for vertice in Graph_verts:
                    counting += 1
                    #print("Comparing all recs from DB ", i," with vertice ", counting, " encoding on vert: ",  vertice)

                    # if vertice already in a cluster with 3 rows then continue

                    self.findMatchesinDB(Db, vertice, indexerExists=indexerExist)

            G_edges = list(self.G.edges)
            print("Initial length of G_edges:", len(G_edges))

            G_edges_weighted = list(self.G.edges(data=True))
            opt_E = nx.max_weight_matching(self.G)
            # iterate edges
            #print("Type of opt_E",type(opt_E))
            check_vals = list(opt_E)
            print("Length of check_vals:", len(check_vals))

            for outer in check_vals:
                resultGraph.add_edge(*outer)
                
            
            
            #resultGraph = self.G
                    
            #iterate remaining edges 
            #merge cluster vertices 
            Result_edges = list(resultGraph.edges)
            print("Size of resultGraph.edges before contraction:", len(Result_edges))
            for edges in list(Result_edges):
                node1 = edges[0]
                node2 = edges[1]
                #print("TYPE OF G: ",type(resultGraph))
                assert type(resultGraph) == nx.graph.Graph

                # if neither node has been used to make a cluster, then:
                potentialCluster1 = self.findIfNodeIsClusterInClusterList(node1)
                if potentialCluster1 != None:
                    potentialCluster1.addOneRowToCluster(node2)
                    cluster = potentialCluster1
                else:
                    potentialCluster2 = self.findIfNodeIsClusterInClusterList(node2)
                    if potentialCluster2 != None:
                        potentialCluster2.addOneRowToCluster(node1)
                        cluster = potentialCluster2
                    else:
                        cluster = self.createNewCluster(node1)
                        cluster.addOneRowToCluster(node2)

                self.listOfClusters.append(cluster)           

                # Figure out how to add cluster if we only updated it.
                
                #resultGraph = nx.contracted_nodes(resultGraph, node1, node2)
            print("Size of result edges after contraction:", len(resultGraph.edges))
                
            
        final_clusters = resultGraph.nodes

       
        print("Created cluster list of length: ", len(self.listOfClusters))
        return self.listOfClusters

    def findIfNodeIsClusterInClusterList(self, node1):
        for cluster in self.listOfClusters:
            for row in cluster.getClusterRowObjList():
                if node1 == row:
                    return cluster
        return None


    def initaliseVertices(self, Db, G):
        # add vertices
        for row in Db:
            assert type(row) == Row
            vert = row#.encodedRowString
            G.add_node(vert)
        
        return list(G.nodes)

    def findMatchesinDB(self, Db, vertice, indexerExists=False):
        foundMatch = False

        if indexerExists:
            rows = self.indexer.getRowsWithAtLeast1SameKey(vertice)
            #print("Comparing vertice with", len(rows), "rows")
            for row in rows:
                assert type(row) == Row
                foundMatch = self.findMatch(row,vertice)
                if foundMatch == True:
                    break                       
                    
        else:
            for row in Db:  
                assert type(row) == Row  
                foundMatch = self.findMatch(row,vertice)
                if foundMatch == True:
                    break    

    def findMatch(self,row,vertice):
        assert row != None
        assert vertice != None
        exactMatch = row.encodedRowString.count(vertice.encodedRowString)
        if exactMatch == 1:
            self.G.add_edge(vertice, row, sim = 1)
            return True
        else:
            sim_val = self.sim(row.encodedRowString, vertice.encodedRowString)
            if sim_val >= self.min_similarity_threshold:
                # add edges
                self.G.add_edge(vertice, row, sim = sim_val)   # This line should be used more carefully to optimise performance
                return True
            else:
                return False

    def createNewCluster(self, row):
        #print(row)
        assert type(row) == Row
        cluster = Cluster(self.clusterId)
        cluster.addOneRowToCluster(row)
        self.clusterId += 1

        return cluster