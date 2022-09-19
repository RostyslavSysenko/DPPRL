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
class graph:
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = []
        self.gdict = gdict
        
    def edges(self):
        return self.findedges()
# Get the keys of the dictionary

    def getVertices(self):
        return list(self.gdict.keys())
    
    def findedges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if (nxtvrtx, vrtx) not in edgename:
                    edgename.append((vrtx, nxtvrtx))
        return edgename
    
    def addVertex(self, vrtx):
        if vrtx not in self.gdict:
            self.gdict[vrtx] = []
    
    def pruneVertex(self, vrtx):
        if vrtx in self.gdict:
            del self.gdict[vrtx]
            
    # Add the new edge
    def AddEdge(self, edge):
        edge = set(edge)
        (vrtx1, vrtx2) = edge
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]
            