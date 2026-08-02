"""
Lightweight probabilistic dedup filter (your notes: #5 Bloom filter -> fast
lookup, dedupe alerts). Used as a cheap in-memory pre-check before we ever
touch Postgres. It can have false positives (rare, tunable via error_rate)
but never false negatives -- so a Postgres unique-constraint lookup is still
the source of truth on a possible hit.
"""
import hashlib
import math


class BloomFilter:
    def __init__(self, capacity: int = 100_000, error_rate: float = 0.001):
        self.size = self._optimal_size(capacity, error_rate)
        self.hash_count = self._optimal_hash_count(self.size, capacity)
        self.bit_array = bytearray(self.size // 8 + 1)

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        return int(-(n * math.log(p)) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hash_count(m: int, n: int) -> int:
        return max(1, int((m / n) * math.log(2)))

    def _hashes(self, item: str):
        for i in range(self.hash_count):
            digest = hashlib.sha256(f"{i}:{item}".encode()).hexdigest()
            yield int(digest, 16) % self.size

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self.bit_array[idx // 8] |= 1 << (idx % 8)

    def might_contain(self, item: str) -> bool:
        return all(self.bit_array[idx // 8] & (1 << (idx % 8)) for idx in self._hashes(item))
