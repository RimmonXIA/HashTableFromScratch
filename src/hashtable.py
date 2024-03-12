from collections import deque
from typing import NamedTuple, Any


class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    @classmethod
    def from_dict(cls, dictionary: dict, capacity=None):
        hash_table = cls(capacity or len(dictionary))
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table

    def __init__(self, capacity=8, load_factor_threshold=0.6) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be a positive number")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number in range (0, 1]")
        self._keys = []
        self._buckets = [deque() for _ in range(capacity)]
        self._load_factor_threshold = load_factor_threshold

    # for `==` and/or `!=`
    def __eq__(self, __value: object) -> bool:
        if self is __value:
            return True
        if type(self) is not type(__value):
            return False
        return set(self.pairs) == set(__value.pairs)

    # for `repr(obj)`
    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    # for `str(obj)`
    def __str__(self) -> str:
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    # handle `for` loops directly
    def __iter__(self):
        yield from self.keys

    # for `len(obj)`
    def __len__(self):
        return len(self.pairs)

    # for `item[key] = value`
    def __setitem__(self, key, value):
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()

        bucket = self._buckets[self._index(key)]
        for index, pair in enumerate(bucket):
            if pair.key == key:
                # if find the old key, update and return
                bucket[index] = Pair(key, value)
                return
        # loop through whole bucket, append the pair
        else:
            self._keys.append(key)
            bucket.append(Pair(key, value))

    def __delitem__(self, key):
        bucket = self._buckets[self._index(key)]
        # test when stores several identical pairs
        for index, pair in enumerate(bucket):
            if pair.key == key:
                self._keys.remove(key)
                del bucket[index]
                break
        else:
            raise KeyError(key)

    # for "item[key]"
    def __getitem__(self, key):
        bucket = self._buckets[self._index(key)]
        for pair in bucket:
            if pair.key == key:
                return pair.value
        raise KeyError(key)

    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._buckets = copy._buckets

    # where all the `hash` magic happens
    def _index(self, key):
        return hash(key) % self.capacity

    # for the 'in' operation
    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    # mimic the 'dict.get()' behavior
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    # for `obj.keys`, should only have unique keys
    @property
    def keys(self):
        return self._keys.copy()

    # for `item.values`, may have & should return duplicate values
    @property
    def values(self):
        return [self[key] for key in self._keys]

    # two tiers loop to get all the pair
    @property
    def pairs(self):
        return [(key, self[key]) for key in self._keys]

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)

    @property
    def capacity(self):
        return len(self._buckets)

    @property
    def load_factor(self):
        occupied = [bucket for bucket in self._buckets if bucket]
        return len(occupied) / self.capacity
