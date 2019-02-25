
import itertools

print(" -- count --")
count = itertools.count(10, 2) # infinite
print(next(count)) # 10
print(next(count)) # 12
print(next(count)) # 14

print(" -- cycle -- ")
cycle = itertools.cycle('ab') # infinite
print(next(cycle)) #a
print(next(cycle)) #b
print(next(cycle)) #a
print(next(cycle)) #b

print(" -- repeat --")
repeat = itertools.repeat('c', 4) # returned iterator repeat 'c' 4 times
print(next(repeat))
print(next(repeat))
print(next(repeat))
print(next(repeat))

print(" ---- chain ----- ")
tee1, tee2 = itertools.tee(iter([1, 2, 3, 4]), 2) # make two(=>2 in argument) iteraters from one iterator

print(next(tee1))
print(next(tee1))
print(next(tee1))
print(next(tee1))
print(next(tee2))
print(next(tee2))
print(next(tee2))
print(next(tee2))

print("-- islice --")
iter1 = iter([1, 2, 3, 4, 5])
iter2 = itertools.islice(iter1, 1, 3) # same as arr[1:3] for iterator iter1
for v in iter2:
    print(v)


print(" -- takewhile --")
# returns iterator which stops when predicate is not satisfied
takewhile = itertools.takewhile(lambda x: x<5, iter([1, 2, 4, 5, 3]))
for v in takewhile:
    print(v, end=" ") # 1 2 4
print("\n")


print(" -- dropwhile -- ")
# returns iterator which starts to return item when predicate is not satisfied.
dropwhile = itertools.dropwhile(lambda x: x<5, iter([1, 2, 4, 5, 3]))
for v in dropwhile:
    print(v, end=" ") # 5 3
print("\n")


print(" -- filterfalse -- ")
# returns iterator which returns items which satisfy predicate. The opossite of filter (filter
# returns also iterator)
filterfalse = itertools.filterfalse(lambda x: x<5, iter([1, 6, 3, 5, 3]))
for v in filterfalse:
    print(v, end=" ") # 6 5
print("\n")

print(" -- product -- ")
product = itertools.product(iter(['a', 'b']), iter(['A', 'B', 'C']))
for v in product:
    print(v, end=" ") # ('a', 'A') ('a', 'B') ('a', 'C') ('b', 'A'), ...
print("\n")


print(" -- permutations --")
permutations = itertools.permutations(iter(['a', 'b', 'c']))
for v in permutations:
    print(v, end=" ") # ('a', 'b', 'c') ('a', 'c', 'b') ('b', 'a', 'c'), ('a', 'c', 'a') ...
print("\n")


print(" -- combinations --")
combinations = itertools.combinations(iter(['a', 'b', 'c']), 2)
for v in combinations:
    print(v, end=" ") # ('a', 'b'), ('a', 'c'), ('b', 'c')
print("\n")

