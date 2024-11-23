import numpy as np
import xxhash

class BloomFilter:
    #constant-space set data structure
    #use to speed up answers in a key-value storage system
    def __init__(self, size, hash_num):
        self.size = size
        self.hash_num = hash_num
        self.bit_array = [0] * size

    def add(self, element):
        # constant time O(k)
        for i in range(self.hash_num -1):
            hash_int = xxhash.xxh64((element.lower() + str(i)).encode()).intdigest()
            index = hash_int % self.size
            self.bit_array[index] = 1
    
    def query(self, element):
        # constant time O(k) completely independent of the number of items already in the set 
        for i in range(self.hash_num -1):
            hash_int = xxhash.xxh64((element.lower() + str(i)).encode()).intdigest()
            index = hash_int % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    def estimate_num_of_items(self): # currently approx. returning half. why?
        ones = self.bit_array.count(1)
        result = - (self.size/self.hash_num) * np.log(1 - (ones/ self.size))
        return result


    def union(self, other):
        if self.size != other.size or self.hash_num != other.hash_num:
            print("bloom filters must be of equal size")
        else:
            result = BloomFilter(self.size, self.hash_num)
            result.bit_array = [self.bit_array[i] | other.bit_array[i] for i in range(0, self.size)]
            return result
    
    def intersection(self, other):
        if self.size != other.size or self.hash_num != other.hash_num:
            print("bloom filters must be of equal size")
        else:
            result = BloomFilter(self.size, self.hash_num)
            result.bit_array = [self.bit_array[i] & other.bit_array[i] for i in range(0, self.size)]
            return result

#if __name__ == "__main__":

