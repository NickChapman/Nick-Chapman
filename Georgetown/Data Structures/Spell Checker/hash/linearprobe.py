class LinearProbeHashMap():
    def __init__(self, *args, **kwargs):
        """
        @param args A list of keys and values of the form "a, 10, b, 3, c, 30,..."
        @param size The size that the table should start at
                    It doesn't matter if the args exceed the size because
                    the table will automatically resize to fix this issue. 
        """
        if "size" in kwargs:
            self.array = [None] * kwargs["size"]
        elif len(args) == 0:
            self.array = [None] * 3
        self.active_nodes = 0
        self.collisions_found = 0
        if len(args) != 0:
            # Populate the map
            # It doesn't matter if they specify a size smaller than the number of args
            # The insertions will rehash and expand the list if necessary
            if(len(args) % 2 != 0):
                raise IndexError("The arguments to the LinearProbeHashMap must be key, value pairs")
            self.array = (len(args) // 2) * [None]
            for i in range(0,len(args), 2):
                key = args[i]
                value = args[i + 1]
                self.insert(key, value)

    @staticmethod
    def fnv1a_64(string):
        """ Hashes a string using the 64 bit FNV1a algorithm

        For more information see:
            https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function
        @param string The key to hash
        @returns Hashed key
        """
        fnv_offset = 0xcbf29ce484222325 # The standard FNV 64 bit offset base
        fnv_prime = 0x100000001b3 # The standard FNV 64 digit prime
        hash = fnv_offset
        uint64_max = 2 ** 64
        # Iterate through the bytes of the string, ie the characters
        for char in string:
            # ord() converts the character to its unicode value
            hash = hash ^ ord(char)
            hash = (hash * fnv_prime) % uint64_max
        return hash

    def compress(self, hash):
        """ Formats the value to fit into the table size

        For now this is done quite simply
        @param hash The hash value to be compressed
        """
        table_size = len(self.array)
        return hash % table_size

    def insert(self, key, value):
        """ Adds a key value pair to the table
        If the load factor gets too high it will automatically double
        the table size and rehash. Hashes with fnv1a_64. 
        Resolves collisions using linear probing.
        @param key The key to insert into the table
        @param value The value that goes with the specified key
        """
        key_hash = self.fnv1a_64(str(key))
        location = self.compress(key_hash)
        collision = False
        while(self.array[location] is not None and self.array[location].key != key):
            collision = True
            location = (location + 1) % len(self.array)
        if collision:
            self.collisions_found += 1
        # It will simply overwrite the value for a key if it is already assigned
        # Just need to check whether active nodes needs to be updated
        if self.array[location] is None:
            self.active_nodes += 1
        self.array[location] = HashNode(key, value)
        if (self.active_nodes / len(self.array)) > (2/3):
            # load factor is too high, rehash with table twice the size
            self.rehash(len(self.array) * 2)

    def find(self, key):
        """ Searches for the given key in the table

        @returns -1 for failure
        @returns location for success
        """
        key_hash = self.fnv1a_64(str(key))
        location = self.compress(key_hash)
        # If the location it hashes to is empty then return -1
        if self.array[location] is None:
            return -1
        # There's something in the way and we need to look
        num_checked = 0
        while (num_checked <= len(self.array) and self.array[location] is not None 
               and self.array[location].key != key):
            location = (location + 1) % len(self.array)
            num_checked += 1
        if self.array[location] is None or num_checked >= len(self.array):
            return -1
        else:
            return location

    def delete(self, key):
        """ Removes a key from the table
        @param key The key to remove from the table
        """
        location = self.find(key)
        if location == -1:
            # Key doesn't exist so nothing to delete
            return
        else:
            self.array[location] = None
            self.active_nodes -= 1

    def rehash(self, new_size):
        """ Creates a new map of size new_size and
            rehashes all of the values into the new table
        @param new_size The size of the new table
        """
        temp = LinearProbeHashMap(size=new_size)
        for item in self.array:
            if item is not None:
                temp.insert(item.key, item.value)
        self.array = temp.array
        self.collisions_found = temp.collisions_found

    def __getitem__(self, key):
        """ Get the value at the specified key
        @param key The key to search for
        @except KeyError Raised when the specified key is not found
        @returns the value at the specified key
        """
        location = self.find(key)
        if location == -1:
            raise KeyError(key)
        else:
            return self.array[location].value

    def __setitem__(self, key, value):
        """ Inserts an item into the table
            OR updates an existing value
        @param key The key for the specified value
        @param value the value to insert into the table
        """
        self.insert(key, value)

    def __iter__(self):
        """ Allows one to iterate through the table's values """
        for item in self.array:
            if item is None:
                yield None
            else:
                yield item.value

class HashNode():
    """ A single key value pair in the map """
    def __init__(self, key, value):
        """ Builds the node 
        @param key The key for the value being stored
        @param value The value to be stored
        """
        self.key = key
        self.value = value