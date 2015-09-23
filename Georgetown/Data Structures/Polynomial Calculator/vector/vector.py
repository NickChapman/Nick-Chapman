from vector.node import Node

class Vector():
    
    # MEMBER VARIABLES
    # sentinel - The start of the LL
    # head == sentinel.next
    # tail == sentinel.prev
    # size -> equal to capacity since it's an LL

    def __init__(self, *args, **kwargs):
        """ Takes an unlimited number of arguments which become the contents of the Vector
            Takes an optional kwarg `typesafe` which can be `True` or `False` """
        # Type safety operations (optional)
        if "typesafe" in kwargs:
            self.typesafe = kwargs["typesafe"]
            if self.typesafe != True and self.typesafe != False:
                raise TypeError("The `typesafe` argument to Vector was not `True` or `False`")
        else:
            self.typesafe = False
        self.sentinel = Node("__SENTINEL__")
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel
        self.size = 0
        if ((not Vector.set_is_same_type(args)) and (self.typesafe == True)):
            raise TypeError("Arguments to the list are not the same type")
        else:
            # Build the list
            for item in args:
                self.insert_rear(item)
            self.size = len(args)
            # NO CAPACITY - Size and capacity are the same by virtue of it being a linked list

    def __getitem__(self, index):
        """ Overloads the [] operator
            Returns the item at the specified index 
            Allows negative indexing so a[-1] gives the last item
            Raises an IndexError if the abs(index) is greater than or equal to the size """
        return self.__getnode(index).value

    def __setitem__(self, index, item):
        """ Overloaded [] for assignment
            Allows negative indexing so a[-1] gives the last item
            Raises an IndexError if the abs(index) is greater than or equal to the size
            Raises a TypeError if the item entered does not match the Vector type and typesafe==True"""
        node = self.__getnode(index)
        if ((not self.item_matches_vector_type(item)) and (self.typesafe == True)):
            raise TypeError("An item was added to the Vector with an incorrect type")
        else:
            node.value = item

    def __getnode(self, index):
        """ Returns the node at the specified index
            Allows negative indexing, a[-1] returns the last item
            Raises an IndexError if the specified index is >= abs(size)
            Raises an IndexError if the Vector is empty """
        if (index >= self.size) or (abs(index) > self.size):
            raise IndexError("Index out of bounds")
        elif index >= 0:
            to_go = index
            node = self.sentinel.next
            while to_go > 0:
                node = node.next
                to_go -= 1
            return node

        elif index < 0:
            to_go = abs(index)
            node = self.sentinel
            while to_go > 0:
                node = node.prev
                to_go -= 1
            return node

    def insert_rear(self, item):
        """ Appends an item to the vector. 
            Raises a TypeError if the type of `item` does not match the type of the Vector
                AND typesafe==True """
        if ((not self.item_matches_vector_type(item)) and (self.typesafe == True)):
            raise TypeError("An item was added to the vector with an incompatible type")
        else:
            temp = Node(item)
            temp.prev = self.sentinel.prev
            temp.next = self.sentinel
            self.sentinel.prev.next = temp
            self.sentinel.prev = temp
            self.size += 1

    def append(self, item):
        """An alias for the insert_rear function"""
        self.insert_rear(item)

    def insert(self, index, item):
        """ Adds an item to the Vector at the specified index thus moving all later
            entries down one index.
            Allows negative indexing so a[-1] is the last item
            Raises an IndexError if the index is >= abs(self.size)
            Raises a TypeError if the type of item does not match the Vector type """
        if abs(index) >= self.size:
            raise IndexError("Index out of bounds")
        elif self.size == 0:
            if index != 0:
                raise IndexError("The vector is empty and only the 0 index is currently active")
            else:
                self.insert_front(item)
        elif ((not self.item_matches_vector_type(item)) and (self.typesafe == True)):
            raise TypeError("An item was added to the vector with an incompatible type")
        else:
            node = self.__getnode(index)
            new_node = Node(item)
            new_node.prev = node.prev
            new_node.next = node
            node.prev.next = new_node
            node.prev = new_node
            self.sze += 1

    def insert_front(self, item):
        """ Prepends an item to the Vector
            Raises a TypeError if the type of item does not match the type of the Vector. """
        if ((not self.item_matches_vector_type(item)) and (self.typesafe == True)):
            raise TypeError("An item was added to the vector with an incompatible type")
        else:
            temp = Node(item)
            temp.next = self.sentinel.next
            temp.prev = self.sentinel
            self.sentinel.next.prev = temp
            self.sentinel.next = temp
            self.size += 1

    def erase(self, index):
        """ Erases the value at the given index
            Allow negative indexing. a.erase(-1) erases the last element
            Raises an IndexError if abs(index) >= size """
        if self.size == 0:
            raise IndexError("The Vector is already empty")
        # __getnode is doing index checking
        node = self.__getnode(index)
        node.next.prev = node.prev
        node.prev.next = node.next
        self.size -= 1

    def erase_rear(self):
        """ Erases the last item in the Vector """
        self.erase(-1)
        
    def erase_front(self):
        """ Erases the first item in the Vector """
        self.erase(0)

    def front(self):
        """ Returns the first value in the Vector """
        return self.__getitem__(0)

    def back(self):
        """ Returns the last value in the Vector """
        return self.__getitem__(-1)

    def at(self, index):
        """ Returns the value at the specified index
            Raises an IndexError if the index is out of bounds """
        return self.__getitem__(index)

    def size(self):
        """ Returns the number of elements currently in the Vector """
        return self.size

    def cap(self):
        """ Returns the number of elements the Vector can currently hold
            Always equal to the size for the linked list implementation """
        return self.capacity

    @property
    def capacity(self):
        """ Returns the number of elements the Vector can currently hold
            Always equal to the size for the linked list implementation """
        return self.size

    # HELPER FUNCTIONS
    def item_matches_vector_type(self, item):
        """ Returns true if the item matches the Vector's items type
            Also returns true if the Vector is currently allocated but empty
            Returns false otherwise """
        if self.size == 0:
            return True
        if not isinstance(item, type(self.sentinel.next.value)):
            return False
        else:
            return True

    @staticmethod
    def set_is_same_type(*args):
        """ Returns true if all of the arguments are the same type as the first argument
            False if they are not all the same type """
        if all(isinstance(item, type(args[0])) for item in args):
            return True
        else:
            return False

    def build_from_list(self, list):
        """Fills an already initialized vector with the values from a list"""
        if self.size != 0:
            raise Exception("build_from_list was used with an already built out Vector")
        if not isinstance(list, type([])):
            raise TypeError("The argument to build_from_list was not a list")
        elif len(list) == 0:
            raise Exception("The list passed to build_from_list is empty")
        for item in list:
            self.insert_rear(item)

    def __len__(self):
        """Overload for len()"""
        return self.size

    def __iter__(self):
        """Makes the Vector an iterable object"""
        current = 0
        while current < self.size:
            yield self.__getitem__(current)
            current += 1