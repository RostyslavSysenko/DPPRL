#from IncrementalClusterInput import * 
#import IncrementalClusterInput
from hungarian_algorithm import algorithm
import random
import numpy as np

# input functions and classes
def order(BF_list): 
    
    result = list(BF_list)
    random.shuffle(result)

    return result

def sim(a, b):
    intersect = np.sum(a*b)
    fsum = np.sum(a)
    ssum = np.sum(b)
    #print(intersect, fsum, ssum) # Debugging
    dice = (2 * intersect ) / (fsum + ssum) # Overflow due to infinitely an growing number that eventually exceeds space in Int32 datatype
    dice = np.mean(dice)
    dice = round(dice, 3) 
    
    return dice  
    
class graph:    
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict
        
    def edges(self):
        return self.findedges()
# Get the keys of the dictionary

    def getVertices(self):
        print("Getting Vertices, length: ", len(self.gdict))
        return list(self.gdict.keys())
    
    def findedges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if (nxtvrtx, vrtx) not in edgename:
                    edgename.append((vrtx, nxtvrtx))
        return edgename
    
    def addVertex(self, vrtx):
        if vrtx not in self.gdict: # Error, unhashable type 'dict'
            self.gdict[vrtx] = []
    
    def pruneVertex(self, vrtx):
        if vrtx in self.gdict:
            del self.gdict[vrtx]
            
    # Add the new edge
    def AddEdge(self, edge):
        assert edge == set(edge)
        if len(edge) < 2:
            pass
        else:
            #print("adding edge")
            (vrtx1, vrtx2) = edge
            if vrtx1 in self.gdict:
                self.gdict[vrtx1].append(vrtx2)
            else:
                self.gdict[vrtx1] = [vrtx2]

    
class StaticLinker:
    def __init__(self):
        self.num_of_parties = 3
        self.DBs = []

        # Initialise graph
        self.graph_elements = {}
        self.G = graph(self.graph_elements)

    def addFirstPartyVertices(self, graph:graph):
        for i in range(self.num_of_parties): 
            #first party 
            if i == 1:
            # iterate records 
                for rec in self.DBs[i]: 
                    self.clus_ID += 1 
                    # add vertices
                    graph.addVertex(rec)

    def staticLinkage(self, database1, database2, database3): # Function needs more abstraction for readability and debugging
            # input 
            # D --> Party 𝑃𝑖’s BFs 
            self.DBs = [database1, database2, database3]

            self.num_of_parties = 3

            # B --> Blocks containing the union of blocks from all parties -> implement later

            # sim --> Similarity function

            # ord --> Ordering function for incremental processing of databases : 

            # map --> one to one mapping algo

            # min_similarity_threshold (st) --> Minimum similarity threshold to classify record sets
            min_similarity_threshold = 0.65
            # min_subset_size (sm) --> Minimum subset size, with 2 ≤ 𝑠𝑚 ≤ 𝑝
            min_subset_size = 2

            # output
            # M - matching clusters
            # intialisation 
            self.clus_ID = 0
            
            M = []

            #order databases 
            self.DBs = order(self.DBs)

            # iterate parties
            self.addFirstPartyVertices(self.G)
            for i in range(2, self.num_of_parties): 
                G_ver = self.G.getVertices()
                # other parties 
                if i > 1:
                    # iterate records 
                    for rec in self.DBs[i]: 
                        # iterate vertices in G (first party)
                        for c in G_ver :
                            # calculate similarity between first party records and other records
                            # Not accounting for Row Object
                            sim_val = sim(int(rec),int(c))
                            if sim_val >= min_similarity_threshold:
                                # add edges - does not match exactly
                                self.G.AddEdge({c, rec})
                                # 1-to-1 mapping 
                                # return a list of matched vertices  
                    
                    G_edge = self.G.edges()
                    opt_E = algorithm.find_matching(self.graph_elements, matching_type = 'max', return_type = 'list')                  
                    
                    # iterate edges
                    check_vals = [X[0] for X in opt_E]

                    for edges in list(G_edge):
                        if edges in check_vals:
                            continue
                        else: 
                            # prune edges 
                            self.G.pruneVertex(edges)
                    
            # Iterate final clusters
            for c in self.graph_elements: 
                # size at least sm
                if int(c) >= min_subset_size:
                    # Add to M 
                    M.append(c)

            # output M - returns list of clusters
            return (" Cluster list: ", M) 


##########################################################################################
#from IncrementalClusterInput import * 
#import IncrementalClusterInput
#from hungarian_algorithm import algorithm
#import random
#import numpy as np
#
## input functions and classes
#def order(BF_list): 
#    
#    result = list(BF_list)
#    random.shuffle(result)
#
#    return result
#
#def sim(a, b):
#    intersect = np.sum(a*b)
#    fsum = np.sum(a)
#    ssum = np.sum(b)
#    dice = (2 * intersect ) / (fsum + ssum)
#    dice = np.mean(dice)
#    dice = round(dice, 3) 
#    
#    return dice  
#    
#class graph:    
#    def __init__(self,gdict=None):
#        if gdict is None:
#            gdict = []
#        self.gdict = gdict
#        
#    def edges(self):
#        return self.findedges()
## Get the keys of the dictionary
#
#    def getVertices(self):
#        return list(self.gdict.keys())
#    
#    def findedges(self):
#        edgename = []
#        for vrtx in self.gdict:
#            for nxtvrtx in self.gdict[vrtx]:
#                if (nxtvrtx, vrtx) not in edgename:
#                    edgename.append((vrtx, nxtvrtx))
#        return edgename
#    
#    def addVertex(self, vrtx):
#        if vrtx not in self.gdict: # Error, unhashable type 'dict'
#            self.gdict[vrtx] = []
#    
#    def pruneVertex(self, vrtx):
#        if vrtx in self.gdict:
#            del self.gdict[vrtx]
#            
#    # Add the new edge
#    def AddEdge(self, edge):
#        assert edge == set(edge)
#        if len(edge) < 2:
#            pass
#        else:
#            (vrtx1, vrtx2) = edge
#            if vrtx1 in self.gdict:
#                self.gdict[vrtx1].append(vrtx2)
#            else:
#                self.gdict[vrtx1] = [vrtx2]
#            
#
#def staticLinkage(database1, database2, database3): 
#    # input 
#    # D --> Party 𝑃𝑖’s BFs 
#    DBs = [database1, database2, database3]
#
#    num_of_parties = 3
#
#    # B --> Blocks containing the union of blocks from all parties -> implement later
#
#    # sim --> Similarity function
#
#    # ord --> Ordering function for incremental processing of databases : 
#
#    # map --> one to one mapping algo
#
#    # min_similarity_threshold (st) --> Minimum similarity threshold to classify record sets
#    min_similarity_threshold = 0.65
#    # min_subset_size (sm) --> Minimum subset size, with 2 ≤ 𝑠𝑚 ≤ 𝑝
#    min_subset_size = 2
#
#    # output
#    # M - matching clusters
#    #intialisation 
#    clus_ID = 0
#    graph_elements = {}
#    G = graph(graph_elements)
#    M = []
#
#    #order databases 
#    DBs = order(DBs)
#
#    # iterate parties
#    for i in range(num_of_parties): 
#        #first party 
#        if i == 1:
#        # iterate records 
#            for rec in DBs[i]: 
#                clus_ID += 1 
#                # add vertices
#                G.addVertex(rec)
#                
#        G_ver = G.getVertices()
#        # other parties 
#        if i > 1:
#            # iterate records 
#            for rec in DBs[i]: 
#                # iterate vertices in G (first party)
#                for c in G_ver :
#                    # calculate similarity between first party records and other records
#                    # Not accounting for Row Object
#                    sim_val = sim(int(rec),int(c))
#                    if sim_val >= min_similarity_threshold:
#                        # add edges - does not match exactly
#                        G.AddEdge({c, rec})
#                        # 1-to-1 mapping 
#                        # return a list of matched vertices  
#            
#            G_edge = G.edges()
#            opt_E = algorithm.find_matching(graph_elements, matching_type = 'max', return_type = 'list')                  
#            
#            # iterate edges
#            check_vals = [X[0] for X in opt_E]
#
#            for edges in list(G_edge):
#                if edges in check_vals:
#                    continue
#                else: 
#                    # prune edges 
#                    G.pruneVertex(edges)
#               
#    # Iterate final clusters
#    for c in graph_elements: 
#        # size at least sm
#        if int(c) >= min_subset_size:
#            # Add to M 
#            M.append(c)
#
#    # output M - returns list of clusters
#    return (" Cluster list: ", M) 