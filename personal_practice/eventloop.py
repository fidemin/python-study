
from queue import Queue
from functools import partial
from time import sleep

eventloop = None

class EventLoop(Queue):
    def start(self):
        while True:
            function = self.get()
            function()


def do_hello():
    global eventloop
    sleep(0.5)
    print("Hello")
    eventloop.put(do_world)


def do_world():
    global eventloop
    sleep(0.5)
    print("world")
    eventloop.put(do_hello)


if __name__ == "__main__":
    eventloop = EventLoop()
    eventloop.put(do_hello)
    eventloop.start()
