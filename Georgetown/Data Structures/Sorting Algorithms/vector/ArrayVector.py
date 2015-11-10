import ctypes

class CtypesArray:
    def __init__(self, *args, **kwargs):
        if "size" in kwargs:
            self.size = kwargs["size"]
            if len(args) > self.size:
                raise OverflowError("The number of items to store has exceed the predesignated size")
        else:
            self.size = len(args)
        self.array = (self.size * ctypes.py_object)()
        for i in range(len(args)):
            self.array[i] = args[i]

    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        else:
            return self.array[index]
            
    def __setitem__(self, index, item):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        else:
            self.array[index] = item

    def erase(self, index):
        # Create a null pointer at the specified index
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        else:
            self.array[index] = ctypes.py_object()

class VectorArray:
    # MEMBER VARIABLES
    # array - a CtypesArray
    # size - Number of items in the Vector
    # capacity - Number of items the Vector can hold

    def __init__(self, *args, **kwargs):
        """ Takes unlimited unnamed arguments that will be used to populate the array.
            Also accepts an optional `cap` key word arg which presets the capacity of the array """
        # Determine the capacity
        if "cap" in kwargs:
            if kwargs["cap"] < len(args):
                raise OverflowError("The number of items to store has exceeded the predesignated capacity")
            self.capacity = kwargs["cap"]
            self.array = CtypesArray(size=self.capacity)
        else:
            self.array = CtypesArray(size=len(args))
            self.capacity = len(args)
        for i in range(len(args)):
            self.array[i] = args[i]
        self.size = len(args)

    def __setitem__(self, index, item):
        """ Used with `a[1] = 10` notation,
            Does not allow `a[1] = None` so this method can not erase items 
            Also does not allow for items to be set in a loose nature:
                a = Vector(10)
                a[9] = 1 # NOT ALLOWED IF a[8] is None """
        # We perform no bounds checking because the array underneath takes care of it
                
        # Check that the index to set is not preceded by empty spaces
        # We use try and except to check for NULL pointers
        # First we have to make sure we aren't at index 0, its an edge case
        if index == 0:
            # nothing to do
            pass
        else:    
            # If we aren't at zero see if the preceding value is empty
            try:
                if self.array[index - 1]:
                    pass        
            except ValueError:
                raise IndexError("The preceding index is still empty")        
        try:
            if self.array[index]:
                pass
        except ValueError:
            self.size += 1
        self.array[index] = item

    def __getitem__(self, index):
        """ Used with a[0] notation for getting
            Simply returns the value at the specified index """
        # Performs no error checking because the array underneath is doing it
        try:
            return self.array[index]
        except ValueError:
            return None

    # REQUIRED METHODS

    def insert_rear(self, item):
        """ Appends an item to the vector after checking to ensure it is the correct type """
        if self.capacity == 0:
            temp = CtypesArray(size=1)
            temp[0] = item
            self.size = 1
            self.capacity = 1
            self.array = temp
        elif self.size < self.capacity:
            self.array[self.size] = item
            self.size += 1
        else:
            temp = CtypesArray(size=(self.capacity * 2))
            for i in range(self.capacity):
                temp[i] = self.array[i]
            temp[self.capacity] = item
            self.capacity *= 2
            self.size += 1
            self.array = temp

    def insert(self, index, item):
        """ Inserts an item into the Vector at the specified index
            Performs type checking to make sure the type is the vector's type
            Shuffles the array to ensure that a compact data structure is maintained """
        if index == 0:
            self.insert_front(item)
        # If an item is added in a non compact way
        elif index != 0:
            try:
                self.array[index -1]
            except ValueError:
                raise IndexError("The index preceding the one entered is still empty. Non compact structure created")
        if self.size >= self.capacity:
            temp = CtypesArray(size=(self.capacity * 2))
            for i in range(self.capacity):
                temp[i] = self.array[i]
            self.capacity *= 2
            self.array = temp
        for i in reversed(range(index, self.size + 1)):
            self.array[i] = self.array[i - 1]
        self.array[index] = item
        self.size += 1
            

    def insert_front(self, item):
        """ Prepends an item to the array after checking if it is a compatible type
            Shuffles the array downwards as necessary to make sure the data structure is compact """
        if self.capacity > 0:
            # Use try/except to see if NULL pointer at 0
            try:
                self.array[0]
            except ValueError:
                self.size += 1
            self.array[0] = item
        else:
            # The array needs to be shuffled down
            # Is there room at the end?
            if self.size < self.capacity:
                # Room at the end, shuffle everything down one
                for i in reversed(range(self.size)):
                    self.array[i+1] = self.array[i]
                self.array[0] = item
                self.size += 1
            else:
                # No room at the end, increase the array size then shuffle
                temp = CtypesArray(size=(self.capacity * 2))
                for i in range(self.capacity):
                    temp[i + 1] = self.array[i]
                temp[0] = item
                self.array = temp
                self.size += 1
                self.capacity *= 2

    def erase(self, index):
        """ Deletes the entry at the given index
            Performs index checking to make sure the specified index is erasable
            Downsizes the space used after if more than 1/2 of the
            entries are free at the end of the array """
        if index == (self.size - 1):
            self.array.erase(index)
            self.size -= 1
            if self.size <= (self.capacity / 2):
                self.downsize()
        else:
            # Clear the specified space
            self.array.erase(index)
            for i in range(index, self.size - 1):
                self.array[i] = self.array[i + 1]
            self.size -= 1
            # Clear the now useless value at the end of the array
            self.array.erase(self.size)
            if self.size <= (self.capacity / 2):
                self.downsize()

    def erase_rear(self):
        """ Erases the last entry in the vector """
        self.erase(self.size - 1)

    def erase_front(self):
        """ Erases the first entry in the vector """
        self.erase(0)

        # REQUIRED ACCESSORS

    def front(self):
        """ Returns the first item in the vector """
        return self.array[0]

    def back(self):
        """ Returns the last item in the vector """
        return self.array[self.size - 1]

    def at(self, index):
        """ Returns the item at the specified index if the index is valid
            Raises IndexError otherwise """
        return self.array[index]

    def size(self):
        """ Returns the number of items currently stored in the Vector """
        return self.size

    def cap(self):
        """ Returns the number of items that can possibly be stored in the Vector """
        return self.capacity

    # HELPER FUNCTIONS
    def fill(self, value):
        """ Fills the entire vector with the given value """
        for i in range(self.capacity):
            self.array[i] = value
        self.size = self.capacity

    def fill_empty(self, value):
        """ Fills the empty space of the vector with the given value """
        for i in range(self.size, self.capacity):
            self.array[i] = value
        self.size = self.capacity

    def clear(self):
        self.array = CtypesArray()
        self.capacity = 0
        self.size = 0

    def downsize(self):
        """ Reduces the capacity of the array to its actual size """
        temp = CtypesArray(size=self.size)
        for i in range(self.size):
            temp[i] = self.array[i]
        self.array = temp

    def print(self):
        """ Prints out each item in the Vector """
        for i in range(self.size):
            print(self.array[i])

    def build_from_list(self, list):
        """Fills an already initialized vector with the values from a list"""
        if self.size != 0:
            raise Exception("build_from_list was used with an already built out Vector")
        if not isinstance(list, type([])):
            raise TypeError("The argument to build_from_list was not a list")
        elif len(list) == 0:
            raise Exception("The list passed to build_from_list is empty")
        # The next format is used to deal with values of "None" filling the end of a list
        for item in list:
            if item is not None:
                self.insert_rear(item)

    def __len__(self):
        """Overload for len()"""
        return self.size

    def __iter__(self):
        """Makes the Vector an iterable object"""
        current = 0
        while current < self.size:
            yield self.array[current]
            current += 1

    def append(self, value):
        self.insert_rear(value)

    ### SORTING METHODS ###
    def insertion_sort(self):
        for i in range(1, self.size):
            inserted_value = self.array[i]
            index = i
            # Move down the array until the value being inserted into place is greater
            # than the value in front of it
            while index > 0 and inserted_value < self.array[index - 1]:
                self.array[index] = self.array[index - 1]
                index -= 1
            # Put the value being inserted into its correct placement in the sorted sublist
            self.array[index] = inserted_value

    def radix_sort(self):
        """Radix sort implemented with an internal bucket sort"""
        try:
            self.array[0]
        except IndexError:
            return
        base = 10
        buckets = VectorArray(cap=10)
        for i in range(10):
            buckets.insert_rear(VectorArray())
        # Get the largest number to sort
        largest_value = self.array[0]
        for i in range(self.size):
            if self.array[i] > largest_value:
                largest_value = self.array[i]
        # Calculate number of digits
        digits = 1
        while (largest_value / base**digits) > 1:
            digits += 1
        for digit in range(digits):
            for i in range(self.size):
                value = self.array[i]
                value = value // base**digit
                buckets[value % base].append(self.array[i])
            temp = VectorArray()
            for bucket in buckets:
                for item in bucket:
                    temp.append(item)
                bucket.clear()
            self.array = temp

    def merge_sort(self):
        """Basic merge sort"""
        try:
            self.array[0]
        except IndexError:
            return
        self.__merge_sort(0, self.size - 1)

    def __merge_sort(self, low, high):
        """Merge sort private call"""
        if low < high:
            mid = (low + high) // 2
            self.__merge_sort(low, mid)
            self.__merge_sort(mid + 1, high)
            self.__merge(low, mid, high)
    
    def __merge(self, low, mid, high):
        """The actual merging function for __merge_sort"""
        left_size = mid - low + 1
        right_size = high - mid
        left = VectorArray(cap=left_size)
        right = VectorArray(cap=right_size)
        for i in range(low, low + left_size):
            left.append(self.array[i])
        for i in range(mid + 1, high + 1):
            right.append(self.array[i])
        left_index = 0
        right_index = 0
        # Infinity is added to the end of the arrays to signify the terminal value
        inf = float("inf")
        left.append(inf)
        right.append(inf)
        # Now left and right are combined back in our primary array
        for i in range(low, high + 1):
            if left[left_index] <= right[right_index]:
                self.array[i] = left[left_index]
                left_index += 1
            else:
                self.array[i] = right[right_index]
                right_index += 1

    # These are not part of the project. They just exist for the sake of existing and practice.
    def counting_sort(self):
        try:
            self.array[0]
        except IndexError:
            return
        self.array = self.__counting_sort(self).array

    def ns_counting_sort(self):
        try:
            self.array[0]
        except IndexError:
            return
        self.array = self.__ns_counting_sort(self).array

    @staticmethod
    def __counting_sort(array):
        """Stable counting sort"""
        # Get the largest value
        largest_value = array[0]
        smallest_value = 0
        for i in range(array.size):
            if array[i] > largest_value:
                largest_value = array[i]
        for i in range(array.size):
            if array[i] < smallest_value:
                smallest_value = array[i]
        # Build our storage array
        # Make sure it is large enough to span the entire set of things
        count = VectorArray(cap=(largest_value - smallest_value + 1))
        count.fill(0)
        # Shift all of the numbers in the original array up by the abs() of the smallest value
        # This is to eliminate negative values while we sort so we can use them to index
        # This will be undone in the end
        for i in range(array.size):
            array[i] += abs(smallest_value)
        # Get a count of each number
        for i in range(array.size):
            count[array[i]] += 1
        count[0] -= 1
        for i in range(1, len(count)):
            count[i] = count[i] + count[i - 1]
        # Now place the values into the temporary array
        temp = [None] * array.size
        for i in range(array.size):
            temp[count[array[i]]] = array[i]
            count[array[i]] -= 1
        array = VectorArray(cap=array.capacity)
        array.build_from_list(temp)
        # Shift the values back down the appropriate amount
        for i in range(array.size):
            array[i] -= abs(smallest_value)
        return array
    
    @staticmethod
    def __ns_counting_sort(array):
        """Non stable counting sort that sorts the list in place"""
        # Get the largest value
        largest_value = array[0]
        smallest_value = 0
        for i in range(array.size):
            if array[i] > largest_value:
                largest_value = array[i]
        for i in range(array.size):
            if array[i] < smallest_value:
                smallest_value = array[i]
        # Build our storage array
        # Make sure it is large enough to span the entire set of things
        count = VectorArray(cap=(largest_value - smallest_value + 1))
        count.fill(0)
        # Shift all of the numbers in the original array up by the abs() of the smallest value
        # This is to eliminate negative values while we sort so we can use them to index
        # This will be undone in the end
        for i in range(array.size):
            array[i] += abs(smallest_value)
        # Get a count of each number
        for i in range(array.size):
            count[array[i]] += 1
        index = 0
        for i in range(len(count)):
            while count[i] > 0:
                array[index] = i
                index += 1
                count[i] -= 1
        for i in range(array.size):
            array[i] -= abs(smallest_value)
        return array