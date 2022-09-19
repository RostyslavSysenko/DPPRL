# input 
import IncrementalClusteringInput
# D --> Party 𝑃𝑖’s BFs along with their BKVs, 1 ≤ 𝑖 ≤ 𝑝
# B --> Blocks containing the union of blocks from all parties
# sim --> Similarity function

# ord --> Ordering function for incremental processing of databases : 

# map --> one to one mapping algo

# min_similarirt_threshold (st) --> Minimum similarity threshold to classify record sets
min_similarirt_threshold = 0.75
# min_subset_size (sm) --> Minimum subset size, with 2 ≤ 𝑠𝑚 ≤ 𝑝
min_subset_size = 2


# output
# M - matching clusters
#intialisation 
clus_ID = 0
G = {}
M = {} 

#order databases 
DBs = ord([])

#iterate blocks 
for i in range(): 
    #graph for block B 
    G[i] = {} 
    # iterate parties
    for i in range(): 
        #first party 
        if i == 1:
        # iterate records 
        for : 
            clus_ID += 1 
            # add vertices
            Gb[clus_ID] = [DBs[i][rec]]


    # other parties 
    if i > 1:
        # iterate records 
        for : 
            # iterate vertices 
            for :
                # calculate similarity 
                sim_val=sim(rec,c)
                if sim_val >= st:
                    # add edges 
                    Gb.add_edge(c, rec)
        # 1-to-1 mapping 
        opt_E = map(Gb.E)

        # iterate edges
        for e :
            if e :
                # prune edges 
                Gb.remove()
    # remaining edges 
    for e :
        # merge cluster vertices 
        Gb.merge(get_vertices(e))
    
# Add B's clusters to G 
G.add(Gb)

# Iterate final clusters
for c : 
    # size at least sm
    if abs(c) > sm:
        # Add to M 
        M.add(c)

# output M 
return M 

# return in data structure