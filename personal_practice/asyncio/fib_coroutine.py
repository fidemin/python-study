import sys
import types

from collections import deque

from eventloop_coroutine import EventLoop
from eventloop_coroutine import print_every

def fib(n):
    if n <= 1:
        yield n
    else:
        a = yield fib(n-1)
        b = yield fib(n-2)
        yield a + b


def result_fibo(fib_gen):
    next_fib = fib_gen.send(None)
    if isinstance(next_fib, types.GeneratorType):
        next_fib2 = fib_gen.send(result_fibo(next_fib))
        if isinstance(next_fib2, types.GeneratorType):
            result = fib_gen.send(result_fibo(next_fib2))
        else:
            return next_fib2
    else:
        return next_fib

    return result


def read_input(loop):
    while True:
        line = yield sys.stdin
        n = int(line)
        fib_n = yield fib(n)
        print("fib({}) = {}".format(n, fib_n))


if __name__ == '__main__':
    '''
    fib_gen = fib(5)
    result = result_fibo(fib_gen)
    print(result)
    '''
    loop = EventLoop()
    hello_task = print_every('Hello world!', 3)
    fib_task = read_input(loop)
    #loop.schedule(hello_task)
    loop.schedule(fib_task)
    loop.run_forever()
