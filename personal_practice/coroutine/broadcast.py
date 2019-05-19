
from coroutine import coroutine, printer
from tailf_grep import grepper, follow

@coroutine
def broadcast(targets):
    while True:
        msg = yield
        for t in targets:
            t.send(msg)


if __name__ == "__main__":
    prn = printer()
    keywords = ('apple', 'error', 'banana')
    filters = [grepper(k, prn) for k in keywords]
    caster = broadcast(filters)

    with open('log.txt') as f:
        for _ in follow(f, caster):
            pass
