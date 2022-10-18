import networkx as nx
import random
import numpy as np
from data_structures.Utilities import *
from data_structures.ClusterList import *
from communication.metrics import *

def order(BF_list): 
    
    result = list(BF_list)
    random.shuffle(result)

    return result

def sim(a, b):
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


def staticLinkage(database1, database2, database3): 
    # input 
    # D --> Party 𝑃𝑖’s BFs 
    DBs = [database1, database2, database3]

    num_of_parties = 3

    # B --> Blocks containing the union of blocks from all parties -> implement later

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
    G = nx.Graph()
    result = []

    #order databases 
    DBs = order(DBs)

    #first party 
    list_len = len(DBs[0])
    #print("FIRST INDEX: ", DBs[0 or 1 or 2][[0,01000011][0,00100111] ... [1,0111010]])
    
    # Populate first 4999
    assert list_len > 4998 & list_len < 5901 # ONLY FOR TESTING, REMOVE THIS LINE
    for x in range(list_len):
        print("Added all records from DB 1 to the graph.")
        #add [1] to get rid of db index
        cluster = DBs[0][x]
        clus_ID += 1 
        # add vertices
        G.add_node(cluster[1])
    
    Graph_verts = list(G.nodes)
    identifiedNonMatches = []

    print("length of graph ", len(Graph_verts))
    dbi =0
    for Db in DBs:
        dbi += 1
        print("length of current Db",len(Db))

        if(Db == DBs[0]):
            continue
        counting = 0
        for vertice in Graph_verts:
            # 
            counting += 1
            print("Comparing with vertice from DB 1: ", counting, " all recs from DB ", dbi," encoding on vert: ",  vertice)
            for rec in Db:
                #recIdx = Db.index(rec)
                if rec[1].count(vertice) >= 1:
                    print("Added record because same rec_id")
                    G.add_edge(vertice, rec[0], sim = 1)
                elif rec in identifiedNonMatches:
                    pass
                else:
                    # calculate similarity between first party records and other records
                    # metrics.testStart() 
                    sim_val = sim(rec[1],vertice)
                    # metrics.testFinish() # Calculate an average time and output with the For vertice line
                    if sim_val >= min_similarity_threshold:
                        # add edges - does not match exactly
                        thisRecordEncoding = rec[1]
                        G.add_edge(vertice, thisRecordEncoding, sim = sim_val)   # This line should be used more carefully to optimise performance


            #G.number_of_nodes
            #print("Vertices compared with: each record in DB[1]")
            # iterate parties
            """
            for i in range(num_of_parties): 
                # other parties 
                if i > 0:
            # iterate records 
            for rec in DBs[i]: 
                # iterate vertices in G (first party)
                for vertice in Graph_verts :
                    #print("won't this print forever?")
                    # calculate similarity between first party records and other records
                    sim_val = sim(rec[1],c)
                    if sim_val >= min_similarity_threshold:
                        # add edges - does not match exactly
                            rec = rec[1]
                            G.add_edge(c, rec, sim = sim_val)  
            """
    
        G_edges_weighted = list(G.edges(data=True))
    
        opt_E = nx.max_weight_matching(G)
        print("weight matching")
        # iterate edges
        check_vals = [X for X in opt_E]

        G_edges = list(G.edges)
        for edges in list(G_edges):
            node1 = edges[0]
            node2 = edges[1]
            if edges in check_vals:
                continue
            else: 
                G.remove_edge(node1, node2)

        #M = nx.Graph() #G # initialise to not break later
        #print("init M")
                
        #iterate remaining edges 
        #merge cluster vertices 
        G_edges = list(G.edges)
        for edges in list(G_edges):
            node1 = edges[0]
            node2 = edges[1]
            assert type(G) == nx.graph
            print("contracting nodes")
            M = nx.contracted_nodes(G, node1, node2)
    #"""
    final_clusters = M.nodes 
    StaticClusters = ClusterList(certaintyThreshold=0.75)

    # Iterate final clusters
    for c in final_clusters: 
        print("length of cluster",len(c), " ", c)
        # size at least sm
        if int(c) >= min_subset_size:
            c = createNewCluster(c)
            StaticClusters.addClusterStaticly(c)
            # Add to result
            result.append(c)

    # output M - returns list of clusters
    #return (" Cluster list: ", result)
    return StaticClusters

def createNewCluster(c):
    print(c)
    clusterFormat = c

    return clusterFormat