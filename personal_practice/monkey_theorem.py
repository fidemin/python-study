import random
from datetime import datetime
random.seed(datetime.now())

def generate_string(strlen):
    seed = "abcdefghijklmnopqrstuvwxyz "
    result = ""
    for _ in range(strlen):
        result += seed[random.randint(0, 26)]
    return result


def score(target, teststr):
    if len(target)> len(teststr):
        long_str = target
        short_str = teststr
    else:
        long_str = teststr
        short_str = target

    matched = 0
    for i, c in enumerate(short_str):
        if long_str[i] == short_str[i]:
            matched += 1

    return matched / len(long_str)

if __name__ == "__main__":
    target = "sheis"
    str_len = len(target)
    string = generate_string(str_len) 

    tries = 1
    while score(target, string) < 1:
        tries += 1
        string = generate_string(str_len)

    print("tries: %d, string: %s" % (tries, string))

