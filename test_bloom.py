import unittest
from bloom import BloomFilter
from recommender import BloomParamRecommender

class TestBloomFilter(unittest.TestCase):

    def setUp(self):
        self.size = 100
        self.hashes = 3
        self.bf = BloomFilter(self.size, self.hashes)

    def test_add_and_query_basic(self):
        self.bf.add("hello")
        self.assertTrue(self.bf.query("hello"), "Added element should probably exist")
        self.assertFalse(self.bf.query("world"), "Non-added element should probably not exist")

    def test_query_empty(self):
        self.assertFalse(self.bf.query("anything"), "Querying empty filter should return False")

    def test_false_positive_rate(self):
        # Add a bunch of elements
        for i in range(50):
            self.bf.add(f"elem{i}")
        false_positives = 0
        # Check elements not added
        for i in range(50, 100):
            if self.bf.query(f"elem{i}"):
                false_positives += 1
        # The false positive count should be low but not zero (probabilistic)
        self.assertLess(false_positives, 10, f"False positives too high: {false_positives}")

    def test_union_and_intersection_size_mismatch(self):
        bf2 = BloomFilter(self.size + 10, self.hashes)
        # Should print warning
        result_union = self.bf.union(bf2)
        self.assertIsNone(result_union, "Union with mismatched size should fail")

    def test_union_and_intersection(self):
        bf2 = BloomFilter(self.size, self.hashes)
        self.bf.add("foo")
        bf2.add("bar")
        union_bf = self.bf.union(bf2)
        self.assertIsNotNone(union_bf)
        self.assertTrue(union_bf.query("foo"))
        self.assertTrue(union_bf.query("bar"))
        inter_bf = self.bf.intersection(bf2)
        self.assertFalse(inter_bf.query("foo"))
        self.assertFalse(inter_bf.query("bar"))

    def test_estimate_num_of_items(self):
        for i in range(10):
            self.bf.add(f"item{i}")
        estimate = self.bf.estimate_num_of_items()
        self.assertGreater(estimate, 0)
        self.assertLess(estimate, 20)

    def test_invalid_inputs(self):
        with self.assertRaises(AttributeError):
            self.bf.add(None)
        with self.assertRaises(AttributeError):
            self.bf.query(None)

class TestBloomParamRecommender(unittest.TestCase):
    
    def test_recommendations(self):
        recommender = BloomParamRecommender(1000, 0.01)
        hashes = recommender.recommend_num_hashes()
        size = recommender.recommend_size()
        bits_per_element = recommender.bits_per_elements()

        self.assertIsInstance(hashes, int)
        self.assertIsInstance(size, int)
        self.assertIsInstance(bits_per_element, float)

        # Basic sanity checks
        self.assertGreater(hashes, 0)
        self.assertGreater(size, 0)
        self.assertGreater(bits_per_element, 0)

if __name__ == "__main__":
    unittest.main()