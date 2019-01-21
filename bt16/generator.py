
from itertools import islice

def i_index_words(text):
    if text:
        yield 0

    for idx, letter in enumerate(text):
        if letter == " ":
            yield idx + 1


text = "Hi, Everybody. I am Yunhong"
it = i_index_words(text)

result = islice(it, 0, 3)

print(list(result))
