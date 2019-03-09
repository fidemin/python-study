from random import normalvariate, random
from itertools import count, groupby
from datetime import date


def read_fake_data():
    for i in count():
        sigma = random() * 10
        yield (i, normalvariate(0, sigma))

def day_grouper(iterable):
    key = lambda value : date.fromtimestamp(value[0])
    return groupby(iterable, key)



data = read_fake_data()

day_groups = day_grouper(data)

c = 0

for k in day_groups:
    print(k)
    c += 1
    if c == 10:
        break
