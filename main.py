import argparse
from bloom import BloomFilter
from recommender import BloomParamRecommender
import os

def count_lines(filename):
    with open(filename, 'r') as f:
        return sum(1 for _ in f)

def build_filter(dictionary_path, size, hash_num):
    bloom = BloomFilter(size, hash_num)
    with open(dictionary_path, "r") as file:
        for line in file:
            word = line.strip()
            if word:
                bloom.add(word)
    print(f"Built bloom filter from '{dictionary_path}'")
    print(bloom)
    return bloom

def interactive_query(bloom):
    print("\nType words to check. Type 'exit' to quit.\n")
    while True:
        word = input("Check word: ").strip()
        if word.lower() == "exit":
            break
        print("Not found!" if not bloom.query(word) else "Might exist!")

def main():
    parser = argparse.ArgumentParser(description="Bloom Filter Spell Checker")
    parser.add_argument("--dict", default="dict.txt", help="Path to dictionary file")
    parser.add_argument("--size", type=int, help="Size of the Bloom filter (bits)")
    parser.add_argument("--hashes", type=int, help="Number of hash functions")
    parser.add_argument("--load", help="Load bloom filter from JSON file")
    parser.add_argument("--save", help="Save bloom filter to JSON file after building")
    parser.add_argument("--fp", type=float, default=0.01, help="Target false positive rate (default 0.01)")

    args = parser.parse_args()

    bloom = None

    if args.load and os.path.exists(args.load):
        bloom = BloomFilter.load(args.load)
        print(f"Loaded bloom filter from {args.load}")
    else:
        num_words = count_lines(args.dict)
        print(f"Dictionary contains {num_words} words")

        # Use recommender only if size or hashes not provided
        if args.size is None or args.hashes is None:
            recommender = BloomParamRecommender(num_words, args.fp)
            size = args.size if args.size is not None else recommender.recommend_size()
            hashes = args.hashes if args.hashes is not None else recommender.recommend_num_hashes()
            print(f"{recommender.recommend()}")
        else:
            size = args.size
            hashes = args.hashes

        bloom = build_filter(args.dict, size, hashes)

        if args.save:
            bloom.save(args.save)
            print(f"Saved bloom filter to {args.save}")

    interactive_query(bloom)

if __name__ == "__main__":
    main()
