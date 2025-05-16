import math

class BloomParamRecommender:
    def __init__(self, num_elements, probability):
        self.num_elements = num_elements
        self.probability = probability

    def recommend_size(self):
        return math.ceil(
            - (self.num_elements * math.log(self.probability)) / (math.log(2) ** 2)
        )

    def recommend_num_hashes(self):
        m = self.recommend_size()
        return math.ceil((m / self.num_elements) * math.log(2))

    def bits_per_element(self):
        return self.recommend_size() / self.num_elements

    def recommend(self):
        return {
            "recommended_size": self.recommend_size(),
            "recommended_hashes": self.recommend_num_hashes(),
            "bits_per_element": round(self.bits_per_element(), 2),
            "false_positive_rate": self.probability,
        }

