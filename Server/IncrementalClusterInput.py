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