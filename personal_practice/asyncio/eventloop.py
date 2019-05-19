from bisect import insort
from collections import namedtuple
import selectors
import sys
from time import time
from util import timed_fib

Timer = namedtuple('Timer', ('timestamp', 'handler'))


class EventLoop(object):
    """ 싱글 스레드 이벤트 루프용 객체
    """
    def __init__(self, *tasks):
        self._running = False
        # self._stdin_handlers는 stdin가 들어올때마다 실행될 handler이다.
        self._stdin_handlers = []
        self._timers = []
        self._selector = selectors.DefaultSelector()
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def run(self):
        self._running = True
        while self._running:
            # IO input이 들어오는지 체크한다.
            for event, mask in self._selector.select(0):
                line = event.fileobj.readline().strip()
                for cb in self._stdin_handlers:
                    cb(line)

            while self._timers and self._timers[0].timestamp < time():
                handler = self._timers[0].handler
                del self._timers[0]
                handler()

    def add_stdin_handler(self, callback):
        self._stdin_handlers.append(callback)

    def add_timer(self, wait_time, callback):
        timer = Timer(timestamp=time() + wait_time, handler=callback)
        insort(self._timers, timer)

    def stop(self):
        self._running = False


if __name__ == "__main__":
    loop = EventLoop()

    def on_std_input(line):
        if line == 'exit':
            loop.stop()
            return
        n = int(line)
        print("fib({}) = {}".format(n, timed_fib(n)))

    def print_hello():
        print("{} - Hello world!".format(int(time())))
        loop.add_timer(3, print_hello)

    loop.add_stdin_handler(on_std_input)
    loop.add_timer(0, print_hello)
    loop.run()


