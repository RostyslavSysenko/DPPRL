import networkx as nx
import random
import numpy as np

def order(BF_list): 
    
    result = list(BF_list)
    random.shuffle(result)

    return result

def sim(a, b):
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
    #print("FIRST INDEX: ", DBs[0][0][0])
    
    for x in range(list_len):
        #add [1] to get rid of db index
        cluster = DBs[0][x]
        clus_ID += 1 
        # add vertices
        G.add_node(cluster[1])
    
    G_ver = list(G.nodes)

    # iterate parties
    for i in range(num_of_parties): 
        # other parties 
        if i > 0:
            # iterate records 
            for rec in DBs[i]: 
                # iterate vertices in G (first party)
                for c in G_ver :
                    # calculate similarity between first party records and other records
                    sim_val = sim(rec[1],c)
                    if sim_val >= min_similarity_threshold:
                        # add edges - does not match exactly
                            rec = rec[1]
                            G.add_edge(c, rec, sim = sim_val)  
    
            G_edges_weighted = list(G.edges(data=True))
        
            opt_E = nx.max_weight_matching(G)
            
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
                    
            #iterate remaining edges 
            #merge cluster vertices 
            G_edges = list(G.edges)
            for edges in list(G_edges):
                node1 = edges[0]
                node2 = edges[1]
                M = nx.contracted_nodes(G, node1, node2)

    final_clusters = M.nodes 
    # Iterate final clusters
    for c in final_clusters: 
        # size at least sm
        if int(c) >= min_subset_size:
            # Add to result
            result.append(c)

    # output M - returns list of clusters
    return (" Cluster list: ", result)