import numpy as np
import xxhash
import json


class BloomFilter:
    #constant-space set data structure
    #use to speed up answers in a key-value storage system
    def __init__(self, size, hash_num):
        self.size = size
        self.hash_num = hash_num
        self.bit_array = np.zeros(size, dtype=bool)

    def add(self, element):
        # constant time O(k)
        for i in range(self.hash_num):
            hash_int = xxhash.xxh64((element.lower() + str(i)).encode()).intdigest()
            index = hash_int % self.size
            self.bit_array[index] = 1
    
    def query(self, element):
        # constant time O(k) completely independent of the number of items already in the set 
        for i in range(self.hash_num):
            hash_int = xxhash.xxh64((element.lower() + str(i)).encode()).intdigest()
            index = hash_int % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    def estimate_num_of_items(self): 
        """
        Estimates the number of elements added to the filter using the formula:
        n ≈ -(m / k) * ln(1 - X/m)
        where:
            m = size of bit array
            k = number of hash functions
            X = number of bits set to 1
        """
        ones = np.count_nonzero(self.bit_array)
        result = - (self.size/self.hash_num) * np.log(1 - (ones/ self.size))
        return result
    
    def estimate_false_positive_rate(self):
        k = self.hash_num
        m = self.size
        n = self.estimate_num_of_items()
        return (1 - np.exp(-k * n / m)) ** k


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
    
    def get_metadata(self):
        ones_count = sum(self.bit_array)
        fill_ratio = ones_count / self.size
        return {
            'size': self.size,
            'hash_num': self.hash_num,
            'bits_set': ones_count,
            'fill_ratio': fill_ratio
        }

    def validate_params(self, expected_num_items, target_fp_rate=0.01):
        from recommender import BloomParamRecommender

        recommender = BloomParamRecommender(expected_num_items, target_fp_rate)
        recommended_size = recommender.recommend_size()
        recommended_hashes = recommender.recommend_num_hashes()

        size_ok = abs(self.size - recommended_size) / recommended_size < 0.1  # within 10%
        hashes_ok = abs(self.hash_num - recommended_hashes) / recommended_hashes < 0.2  # within 20%

        return {
            'size_ok': size_ok,
            'hashes_ok': hashes_ok,
            'recommended_size': recommended_size,
            'recommended_hashes': recommended_hashes
        }
        
    def save(self, filename):
        packed_bits = np.packbits(np.array(self.bit_array, dtype=bool))
        data = {
            "size": self.size,
            "hash_num": self.hash_num,
            "bit_array": packed_bits.tolist(),  # compact storage
            "metadata": {
                "bits_set": np.count_nonzero(self.bit_array),
                "fill_ratio": round(np.count_nonzero(self.bit_array) / self.size, 4)
            }
        }
        with open(filename, "w") as f:
            json.dump(data, f)
    
    @classmethod
    def load(cls, filename):
        import json
        import numpy as np

        with open(filename, "r") as f:
            data = json.load(f)

        bf = cls(data["size"], data["hash_num"])

        packed = np.array(data["bit_array"], dtype=np.uint8)
        unpacked = np.unpackbits(packed)[:data["size"]]  # trim to correct size
        bf.bit_array = unpacked.tolist()

        return bf

        
    def __repr__(self):
        ones = np.count_nonzero(self.bit_array)
        return (
            f"<BloomFilter size={self.size}, hash_num={self.hash_num}, "
            f"bits_set={ones}, fill_ratio={ones / self.size:.4f}>"
        )

