
from threading import Thread
import select
from time import time

def slow_systemcall():
    print("before select")
    select.select([], [], [], 0.1)
    print("after select")

if __name__ == "__main__":
    start = time()
    threads = []
    for _ in range(5):
        thread = Thread(target=slow_systemcall)
        print("thread start")
        thread.start()
        threads.append(thread)

    print("before join")
    # doing something here. time consuming

    for thread in threads:
        thread.join()

    print("after join")
    end = time()
    print("Took %.3f seconds" % (end-start))
