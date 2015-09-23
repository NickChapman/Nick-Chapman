from vector.vector import Vector

class Stack:
    """An implementation of the typical stack data structure"""

    def __init__(self, *args):
        self.storage = Vector()
        if len(args) != 0:
            for item in args:
                self.storage.append(item)

    def clear(self):
        """Clears the entire contents of the stack"""
        self.storage = Vector()

    def is_emtpy(self):
        return self.is_emtpy

    @property
    def is_empty(self):
        if len(self.storage) == 0:
            return True
        else:
            return False

    def push(self, item):
        """Adds an item to the top of the stack"""
        self.storage.append(item)

    def pop(self):
        """Removes an item from the top of the stack"""
        self.storage.erase_rear()

    def top(self):
        """Returns the item at the top of the stack"""
        return self.storage.back()

