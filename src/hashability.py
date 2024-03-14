#%%
class Person:
    def __init__(self, name):
        self.name = name
        self.__self_intro("__init__()")

    def __eq__(self, other):
        self.__self_intro("__eq__()")
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        # return hash(self) == hash(other)
        return self.name == other.name

    def __hash__(self):
        self.__self_intro("__hash__()")
        return hash(self.name)

    def __self_intro(self, prefix=""):
        print(f"{self}.{prefix}:\n\tname: \"{self.name}\"\n\thash_value: \"{hash(self.name)}\"")


#%%
bob = Person("bob")
#%%
employees = {bob: "engineer"}
#%%
employees
#%%
hash(bob)
#%%
employees[bob]
#%%
employees[Person("bob")]
#%%
employees[Person("Bobby")]
#%%
bob.name = "Bobby"
employees[bob]
#%%
employees[Person("bob")]
#%%
bob.name = "bob"
employees[bob]
