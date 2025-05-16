# Spell Checker with Bloom Filter

A memory-efficient spell checker built using a **Bloom filter** — a probabilistic data structure for fast set membership checks with minimal memory usage. This command-line tool allows you to test whether a word might exist in a dictionary.

Based on the [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) algorithm.

---

## Features

- Fast constant-time insertions and lookups
- Probabilistic membership checking (no false negatives, possible false positives)
- Bloom filter persistence (save/load from JSON)
- Automatic parameter recommendation based on expected item count and desired false positive rate
- Set operations: union, intersection
- CLI interface and optional metadata output
- Logging and unit tests for development and debugging

Written in Python, using `xxhash` for fast, consistent hashing and `numpy` for efficiency.

---

## Run the Spell Checker

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the spell checker from the command line:

```bash
python main.py --dict dict.txt

```

You can also save or load filters:

```bash
python main.py --dict dict.txt --save bloom.json
python main.py --load bloom.json

```

Interactive CLI session:
```bash
Type words to check. Type 'exit' to quit.

Check word: pinapple
Might exist!
Check word: bubblebee
Not found!
```
---

## What is a Bloom Filter?

A **Bloom filter** is a space-efficient probabilistic data structure used to test whether an element is likely to be a member of a set.

- It **may return false positives**, but **never false negatives**.
- Commonly used in caching, databases, search engines, and distributed systems.

---

## Example Usage

```python
from bloom import BloomFilter
from recommender import BloomParamRecommender

# Create a bloom filter with a size of 1000 bits and 4 hash functions
bf = BloomFilter(size=1000, hash_num=4)

# Add a word
bf.add("apple")

# Query membership 
print(bf.query("apple"))    # likely true
print(bf.query("banana"))   # likely false

# Get an estimate number of inserted items
print(bf.estimate_num_of_items())

# Combine two filters (union)
bf2 = BloomFilter(size=1000, hash_num=4)
bf2.add("banana")
combined = bf.union(bf2)