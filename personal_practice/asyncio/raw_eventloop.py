
from selectors import DefaultSelector, EVENT_READ
import sys
from time import time

from util import timed_fib

def print_hello():
    print("{} - Hello world!".format(int(time())))


def process_input(stream):
    text = stream.readline()
    n = int(text.strip())
    print('fib({}) = {}'.format(n, timed_fib(n)))


def main():
    selector = DefaultSelector()
    selector.register(sys.stdin, EVENT_READ)
    last_hello = 0
    while True:
        for event, mask in selector.select(0.1):
            process_input(event.fileobj)

        if time() - last_hello > 3:
            last_hello = time()
            print_hello()


if __name__ == "__main__":
    main()
