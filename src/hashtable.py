
BLANK = object()

class HashTable:
    def __init__(self, capacity) -> None:
        self.values = capacity * [BLANK]
    
    def __len__(self):
        return len(self.values)
    
    def __setitem__(self, key, value):
        idx = hash(key) % len(self)
        self.values[idx] = value
    
    def __getitem__(self, key):
        idx = hash(key) % len(self)
        value = self.values[idx]
        if value is BLANK:
            raise KeyError(key)
        return value
    
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