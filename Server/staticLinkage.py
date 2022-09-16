from IncrementalClusterInput import * 
from hungarian_algorithm import algorithm
import random
import numpy as np

def order(BF_list): 
    
    result = list(BF_list)
    random.shuffle(result)

    return result

def sim(a, b):
    intersect = np.sum(a*b)
    fsum = np.sum(a)
    ssum = np.sum(b)
    dice = (2 * intersect ) / (fsum + ssum)
    dice = np.mean(dice)
    dice = round(dice, 3) 
    
    return dice  

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
    min_similarity_threshold = 0.70
    # min_subset_size (sm) --> Minimum subset size, with 2 ≤ 𝑠𝑚 ≤ 𝑝
    min_subset_size = 2

    # output
    # M - matching clusters
    #intialisation 
    clus_ID = 0
    G = {}
    M = []

    #order databases 
    DBs = order(DBs)

    # iterate parties
    for i in range(num_of_parties): 
        #first party 
        if i == 1:
        # iterate records 
            for rec in DBs[i]: 
                clus_ID += 1 
                # add vertices
                G[clus_ID] = [rec]
        
        # other parties 
        if i > 1:
            # iterate records 
            for rec in DBs[i]: 
                # iterate vertices 
                for c in G :
                    # calculate similarity 
                    sim_val = sim(int(rec),c)
                    if sim_val >= min_similarity_threshold:
                        # add edges 
                        G[c].append(rec)
                        # 1-to-1 mapping 
                        # return a list of matched vertices  
            opt_E = algorithm.find_matching(G, matching_type = 'max', return_type = 'list')                  
            
            # iterate edges
            for edges in list(G):
                if edges not in list(opt_E)[1]:
                    # prune edges 
                    G.pop(edges)
            
               
    # Iterate final clusters
    for c in G: 
        # size at least sm
        if abs(c) >= min_subset_size:
            # Add to M 
            M.add(c)

    # output M - returns list of clusters
    return ("Cluster list: ", M) 