from functools import wraps

def coroutine(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return wrap


@coroutine
def printer():
    while True:
        value = yield
        print(value, end="")

if __name__ == "__main__":
    prn = printer()
    prn.send("what?\n")
    prn.send("what??\n")


