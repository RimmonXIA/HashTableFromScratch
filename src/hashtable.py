from typing import NamedTuple, Any

class Pair(NamedTuple):
    key: Any
    value: Any

class HashTable:
    def __init__(self, capacity) -> None:
        self.pairs = capacity * [None]
        
    def __len__(self):
        return len(self.pairs)
    
    def __setitem__(self, key, value):
        self.pairs[self._index(key)] = Pair(key, value)
    
    # for "item[key]"
    def __getitem__(self, key):
        pair = self.pairs[self._index(key)]
        if pair is None:
            raise KeyError(key)
        return pair.value

    def __delitem__(self, key):
        if key in self:        
            self[key] = None
        else:
            raise KeyError(key)
        
        # self.values[self._index(key)] = BLANK
    
    def _index(self, key):
        return hash(key) % len(self)
    
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
    