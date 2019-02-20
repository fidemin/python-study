from threading import Thread, Lock
import time

class LockCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset=1):
        self.count += offset


def worker(sensor_index, how_many, counter):
    threads = []
    for _ in range(how_many):
        counter.increment(1)


    for thread in threads:
        thread.join()


def run_threads(func, how_many, counter):
    threads = []

    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=worker, args=args)
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()


if __name__ == "__main__":
    how_many = 10**5
    #counter = Counter()
    counter = LockCounter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))
