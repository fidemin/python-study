from bisect import insort
from collections import deque, namedtuple
from functools import partial
import selectors
import sys
from time import time
import types

from util import timed_fib


Timer = namedtuple('Timer', ['timestamp', 'handler'])


class SleepForSeconds(object):
    """Yield an object of this type from a coroutine to have it "sleep" for the
    given number of seconds.
    """
    def __init__(self, wait_time):
        self._wait_time = wait_time


class EventLoop(object):
    def __init__(self, *tasks):
        self._running = False

        # Queue of functions scheduled to run
        self._tasks = deque(tasks)

        # (coroutine, stack) pair of tasks waiting for input from stdin
        self._tasks_waiting_on_stdin = []

        # List of (time_to_run, task) pairs, in sorted order
        self._timers = []

        # Register for polling stdin for input to read
        self._selector = selectors.DefaultSelector()
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def resume_task(self, coroutine, value=None, stack=()):
        result = coroutine.send(value)
        print(coroutine, result, stack)

        if isinstance(result, types.GeneratorType):
            self.schedule(result, None, (coroutine, stack))
        elif isinstance(result, SleepForSeconds):
            self.schedule(coroutine, None, stack, time() + result._wait_time)
        elif result is sys.stdin:
            self._tasks_waiting_on_stdin.append((coroutine, stack))
        elif stack:
            # result가 숫자가 나온 경우
            self.schedule(stack[0], result, stack[1])

    def schedule(self, coroutine, value=None, stack=(), when=None):
        """Schedule a coroutine task to be run, with value to be sent to it, and
        stack containing the coroutines that are waiting for the value yielded
        by this coroutine.
        """

        # Bind the parameters to a function to be scheduled as a function with
        # no parameters.
        task = partial(self.resume_task, coroutine, value, stack)
        if when:
            insort(self._timers, Timer(timestamp=when, handler=task))
        else:
            self._tasks.append(task)

    def stop(self):
        self._running = False

    def do_on_next_tick(self, func, *args, **kwargs):
        self._tasks.appendleft(partial(func, *args, **kwargs))

    def run_forever(self):
        self._running = True
        while self._running:
            # First check for available IO input
            for key, mask in self._selector.select(0):
                line = key.fileobj.readline().strip()
                for task, stack in self._tasks_waiting_on_stdin:
                    self.schedule(task, line, stack)
                self._tasks_waiting_on_stdin.clear()

            # Next, run the next task
            if self._tasks:
                task = self._tasks.popleft()
                task()

            # Finally run time scheduled tasks
            while self._timers and self._timers[0].timestamp < time():
                task = self._timers[0].handler
                del self._timers[0]
                task()

        self._running = False


def print_every(message, interval):
    """Coroutine task to repeatedly print the message at the given interval
    (in seconds)
    """
    while True:
        print("{} - {}".format(int(time()), message))
        yield SleepForSeconds(interval)


def read_input(loop):
    """Coroutine task to repeatedly read new lines of input from stdin, treat
    the input as a number n, and calculate and display fib(n).
    """

    while True:
        line = yield sys.stdin
        if line == 'exit':
            loop.do_on_next_tick(loop.stop)
            continue
        n = int(line)
        print("fib({}) = {}".format(n, timed_fib(n)))


if __name__ == '__main__':
    loop = EventLoop()
    hello_task = print_every('Hello world!', 3)
    fib_task = read_input(loop)
    loop.schedule(hello_task)
    loop.schedule(fib_task)
    loop.run_forever()
