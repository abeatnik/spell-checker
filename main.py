from bloomfilter import BloomFilter
from bloom_param_recommender import BloomParamRecommender

bloom = BloomFilter(500, 2)
print(bloom)

file = open("dict-test.txt", "r")

for line in file:
    bloom.add(line)


print(bloom.query("abruptly"))
print(bloom.query("dfghjkk"))


# print(bloom.query("hello"))
# print(bloom.query("dinosaur"))
# print(bloom.query("fghjkl"))
# print(bloom.query("hellooooo"))



# bloom_size = BloomParamRecommender(235976, 0.01)
# print(bloom_size.recommend_num_hashes()) #7
# print(bloom_size.recommend_size()) #2261844
# print(bloom_size.bits_per_elements())
