import asyncio
import sys
from time import time
from util import timed_fib


def process_input():
    text = sys.stdin.readline()
    n = int(text)
    print('fib({}) = {}'.format(n, timed_fib(n)))


async def print_hello():
    while True:
        print("{} - Hello world!".format(int(time())))
        await asyncio.sleep(3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, process_input)
    loop.run_until_complete(print_hello())
