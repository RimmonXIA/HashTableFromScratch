
BLANK = object()

class HashTable:
    def __init__(self, capacity) -> None:
        self.values = capacity * [BLANK]
    
    def __len__(self):
        return len(self.values)
    
    def __setitem__(self, key, value):
        self.values[self._index(key)] = value
    
    def __getitem__(self, key):
        value = self.values[self._index(key)]
        if value is BLANK:
            raise KeyError(key)
        return value

    def __delitem__(self, key):
        if key in self:        
            self[key] = BLANK
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
    