from typing import NamedTuple, Any

DELETED = object()

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    def __init__(self, capacity) -> None:
        if capacity > 1:
            self._slots = capacity * [None]
        else:
            raise ValueError(capacity)

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
        # loop through the hash table until:
        #   - find an never-used slot
        #   - find the slot holds the pair with the matching key
        #   - traverse the hash table
        # this strategy made the slot disposable
        for index, pair in self._probe(key):
            if pair == DELETED:
                continue
            if pair is None or pair.key == key:
                self._slots[index] = Pair(key, value)
                break
        else:
            raise MemoryError((key, value))

    # for "item[key]"
    def __getitem__(self, key):
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value

    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                break
        else:
            raise KeyError(key)

    # where all the `hash` magic happens
    def _index(self, key):
        return hash(key) % self.capacity

    # use linear probing to handle hash collision
    def _probe(self, key):
        # loop through the full hash table
        # start from the current key
        index = self._index(key)
        # covers the full range
        for index in range(self.capacity):
            # return index, pair once a time
            yield index, self._slots[index]
            index = (index + 1) % self.capacity

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

    # defensive copy.
    # only return non-None pairs
    # pair shall be unique because of the the unique of the key
    @property
    def pairs(self):
        return {pair for pair in self._slots if pair not in (None, DELETED)}

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)

    # for `item.values`, may have & should return duplicate values
    @property
    def values(self):
        return [pair.value for pair in self.pairs]
    
    # for `obj.keys`, should only have unique keys
    @property
    def keys(self):
        return {pair.key for pair in self.pairs}

    @property
    def capacity(self):
        return len(self._slots)

    @classmethod
    def from_dict(cls, dictionary: dict, capacity=None):
        # hash_table = cls(capacity) if capacity else cls(len(dictionary) * 10)
        hash_table = cls(capacity or len(dictionary) * 10)
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table