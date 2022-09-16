import numpy as np
import random


def order(BF_list): 
    result = list(BF_list)
    random.shuffle(result)
    return result