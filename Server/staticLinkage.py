from IncrementalClusterInput import * 
from hungarian_algorithm import algorithm


def staticLinkage(): 
    # input 
    # D --> Party 𝑃𝑖’s BFs along with their BKVs, 1 ≤ 𝑖 ≤ 𝑝
    DBs = []

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
    G = {}
    M = {} 

    #order databases 
    DBs = order()

    #iterate blocks 
    for i in range(): 
        #graph for block B 
        G[i] = {} 
        # iterate parties
        for i in range(num_of_parties): 
            #first party 
            if i == 1:
            # iterate records 
                for rec in DBs[i]: 
                    clus_ID += 1 
                    # add vertices
                    G[clus_ID] = [DBs[i][rec]]


            # other parties 
            if i > 1:
                # iterate records 
                for rec in DBs[i]: 
                    # iterate vertices 
                    for c in G :
                        # calculate similarity 
                        sim_val = sim(rec,c)
                        if sim_val >= min_similarity_threshold:
                            # add edges 
                            G.add_edge(c, rec)
                # 1-to-1 mapping 
                opt_E = algorithm.find_matching(G.E, matching_type = 'max', return_type = 'list')

                # iterate edges
                for e in G.E :
                    if e not in opt_E:
                        # prune edges 
                        G.remove()

        # remaining edges 
        for e in G.E :
            # merge cluster vertices 
            G.merge(get_vertices(e))
        
    # Add B's clusters to G 
    G.add(G)

    # Iterate final clusters
    for c in G: 
        # size at least sm
        if abs(c) > min_subset_size:
            # Add to M 
            M.add(c)

    # output M 
    return M 

    # return in data structure