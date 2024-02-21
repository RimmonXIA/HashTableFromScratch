
class HashTable:
    def __init__(self, capacity) -> None:
        self.capacity = capacity
    
    def __len__(self):
        return self.capacity