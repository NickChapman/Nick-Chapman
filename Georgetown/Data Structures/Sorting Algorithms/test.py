from vector.ArrayVector import VectorArray

unsorted_list = [12340981234,2349823,1209475,123,234,34,45,567,67,6,2,5,8,3,1,2,7,9,10,200,13,245,9823,-1]

tests = VectorArray()

for i in range(3):
    tests.append(VectorArray())
    tests[i].build_from_list(unsorted_list)

print("Numbers before sorting")
for item in tests[0]:
    print(item, end=", ")
print("")
tests[0].insertion_sort()
print("After insertion sort")
for item in tests[0]:
    print(item, end=", ")
print("")

tests[1].merge_sort()
print("After merge sort")
for item in tests[1]:
    print(item, end=", ")
print("")

tests[2].radix_sort()
print("After radix sort")
for item in tests[0]:
    print(item, end=", ")
print("")
