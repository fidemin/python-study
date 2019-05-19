
def value_changer(start_value):
    while True:
        start_value = yield start_value


def test():
    a = yield "1"
    b = yield "2"
    print(a, b)
    yield (a, b)


if __name__ == "__main__":
    vc = value_changer("1")
    print(next(vc))
    print(vc.send("2"))

    t = test()
    print(next(t))
    print(t.send("good1"))
    print(t.send("good2"))
