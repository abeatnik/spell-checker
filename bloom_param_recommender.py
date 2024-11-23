import numpy as np
import math

class BloomParamRecommender:
    def __init__(self, num_elements, probability):
        self.num_elements = num_elements
        self.probability = probability

    def recommend_num_hashes(self): 
        k = - np.log(self.probability)/np.log(2)
        return math.ceil(k)

    def bits_per_elements(self): 
        return -2.08 * np.log(self.probability)

    def recommend_size(self): 
        filter_size = - ((self.num_elements * np.log(self.probability))/pow(np.log(2),2))
        return round(filter_size)


    
    
    #value of k that minimizes the false positive probability
    #k = (m/n) * np.log(2)

