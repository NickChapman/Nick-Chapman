from vector.ArrayVector import VectorArray
import ctypes, random, time

input_sizes = [10000, 20000, 40000, 80000, 100000]
sort_types = ["merge sort", "radix sort"]

# Our not insertion sorts run first because they're quick
for i in range(2):
    for size in input_sizes:
        random_list = VectorArray(cap=size)
        for j in range(size):
            random_list.append(random.randrange(0, size, 1))
        start_time = time.time()
        if i == 0:
            random_list.merge_sort()
        else:
            random_list.radix_sort()
        end_time = time.time()
        run_time = end_time - start_time
        print("Time to sort " + str(size) + " items with " + sort_types[i] + ": " + str(run_time))

# Insertion sort runs on its own because it's terribly slow and I had to split execution up
for size in input_sizes:
    random_list = VectorArray(cap=size)
    for j in range(size):
        random_list.append(random.randrange(0, size, 1))
    start_time = time.time()
    random_list.insertion_sort()
    end_time = time.time()
    run_time = end_time - start_time
    print("Time to sort " + str(size) + " items with insertion sort: " + str(run_time))
