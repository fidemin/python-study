from itertools import zip_longest

names = ["Yunhong Min", "Julia", "Typhoon"]
count = (len(name) for name in names)

max_count = 0
max_name = ""

# in python3 zip generates lazy iterator
for name, count in zip(names, count):
    if count > max_count:
        max_count = count
        max_name = name

print(max_name, max_count)


names = ["Yunhong Min", "Julia", "Typhoon"]
count = [len(name) for name in names]
names.append("abcdef")

max_count = 0
max_name = ""

# in python3 zip generates lazy iterator
for name, count in zip_longest(names, count):
    print(name, count)
    if count and count > max_count:
        max_count = count
        max_name = name

print(max_name, max_count)
