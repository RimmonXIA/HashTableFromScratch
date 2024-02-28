#%% 

from typing import NamedTuple, Any

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    def __init__(self, capacity) -> None:
        if capacity > 1:
            self._slots = capacity * [None]
        else:
            raise ValueError(capacity)
    # for `len(obj)`
    def __len__(self):
        return len(self.pairs)

    # for `item[key] = value`
    def __setitem__(self, key, value):
        self._slots[self._index(key)] = Pair(key, value)

    # for "item[key]"
    def __getitem__(self, key):
        pair = self._slots[self._index(key)]
        if pair is None:
            raise KeyError(key)
        return pair.value

    def __delitem__(self, key):
        if key in self:
            self._slots[self._index(key)] = None
        else:
            raise KeyError(key)

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

    # defensive copy.
    # only return non-None pairs
    # pair shall be unique because of the the unique of the key
    @property
    def pairs(self):
        return {pair for pair in self._slots if pair}

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

# #%%
# hash_table = HashTable(capacity=100)

# # %%
# hash_table["missing_key"]
# # %%
