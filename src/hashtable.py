
BLANK = object()

class HashTable:
    def __init__(self, capacity) -> None:
        self.values = capacity * [BLANK]
    
    def __len__(self):
        return len(self.values)
    
    def __setitem__(self, key, value):
        idx = hash(key) % len(self)
        self.values[idx] = value