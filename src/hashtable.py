
class HashTable:
    def __init__(self, capacity) -> None:
        self.values = capacity * [None]
    
    def __len__(self):
        return len(self.values)