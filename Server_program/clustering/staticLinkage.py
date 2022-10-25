from mailcap import findmatch
import networkx as nx
import random
import numpy as np
import sys, os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parentdir)
from data_structures.Utilities import *
from communication.metrics import *
from data_structures.Indixer import *


class staticLinker:
    def __init__(self, simThreshold=0.75, indexer=None):
        self.min_similarity_threshold = simThreshold
        self.G = nx.Graph()
        self.listOfClusters = []
        self.clusterId = 0
        self.indexer = indexer

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
        self.G = nx.Graph()
        #result = []

        # order databases 
        # choose between random_order or sorted_order 
        # sorted_order is more efficient
        DBs = self.random_order(DBs)
       
       # Needs explanation here
        for i in range(num_of_parties-1):
            Graph_verts = self.initaliseVertices(DBs[i])

            print("length of graph ", len(Graph_verts))
            dbi = 0
            # for DB in index > i 
            for Db in DBs:
                if DBs.index(Db) <= i:
                    continue
                if dbi <= i:
                    continue
                dbi += 1
                print("length of current Db: ",len(Db))


                counting = 0
                for vertice in Graph_verts:
                    counting += 1
                    print("Comparing all recs from DB ", dbi," with vertice ", counting, " encoding on vert: ",  vertice)
                    self.findMatchesinDB(Db, vertice)

            opt_E = nx.max_weight_matching(self.G)
            print("weight matching")
            # iterate edges
            check_vals = [X for X in opt_E]
            print("Length of check_vals:", len(check_vals))

            G_edges = list(self.G.edges)
            print("Size of G_edges before purging:", len(G_edges))
            for edges in list(G_edges):
                node1 = edges[0]
                node2 = edges[1]
                if edges in check_vals:
                    continue
                else: 
                    self.G.remove_edge(node1, node2)
                    
            #iterate remaining edges 
            #merge cluster vertices 
            G_edges = list(self.G.edges)
            print("Size of G_edges before contraction:", len(G_edges))
            for edges in list(G_edges):
                node1 = edges[0]
                node2 = edges[1]
                #print("TYPE OF G: ",type(G))
                assert type(self.G) == nx.graph.Graph
                #print("contracting nodes")
                cluster = self.createNewCluster(node1)
                cluster.addOneRowToCluster(node2)
                self.listOfClusters.append(cluster)
                self.G = nx.contracted_nodes(self.G, node1, node2)
            print("Size of G_edges after contraction:", len(G_edges))
                
            
        
        final_clusters = self.G.nodes

 
        #print("Created cluster list of length: ", len(final_clusters))

        # Iterate final clusters
        for c in final_clusters: 
            #print("length of cluster",len(c), " ", c)
            # size at least sm
            #print(len(c))
            clus = self.createNewCluster(c)
            lenOfClus = clus.getNumberOfStoredRows()
            if  lenOfClus >= min_subset_size:
                self.listOfClusters.append(c)
                print(c)

        # output M - returns list of clusters
        #return (" Cluster list: ", result)
        print("Created cluster list of length: ", len(self.listOfClusters))
        return self.listOfClusters

    def initaliseVertices(self, Db):
        # add vertices
        for row in Db:
            vert = row#.encodedRowString
            self.G.add_node(vert)
        return list(self.G.nodes)

    def findMatchesinDB(self, Db, vertice):
        indexerExists = False
        if self.indexer != None:
            assert type(self.indexer) == Indexer
            self.indexer.initialIndexBuild(Db)
            indexerExists = True
            print("USING INDEXER")

        foundMatch = False
        if indexerExists:
            rows = self.indexer.getRowsWithAtLeast1SameKey(row)
            for row in rows:
                foundMatch = self.findMatch()
                if foundMatch == True:
                    break    
        else:
            for row in Db:    
                foundMatch = self.findMatch()
                if foundMatch == True:
                    break    
            

    def findMatch(self,row,vertice):
        exactMatch = row.count(vertice)
        if exactMatch == 1:
            print("Added record to graph because exact same encoding")
            self.G.add_edge(vertice, row, sim = 1)
            return True
        else:
            # calculate similarity between first party records and other records
            # metrics.testStart() 
            sim_val = self.sim(row.encodedRowString,vertice.encodedRowString)
            # metrics.testFinish() # Calculate an average time and output with the For vertice line
            if sim_val >= self.min_similarity_threshold:
                # add edges - does not match exactly
                
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