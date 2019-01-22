
def generator():
    a = [1, 2]
    for i in a:
        yield i


if __name__ == "__main__":
    a = generator()
    print(next(a))
    print(next(a))
    print(next(a))

