from queue import Queue
from threading import Thread
import time

in_queue = Queue()

def consumer():
    time.sleep(0.1)
    #in_queue.get()
    print('Consumer got 1')
    #in_queue.get()
    print('Consumer got 2')
    in_queue.task_done()
    in_queue.task_done()
    print('Consumer done')


thread = Thread(target=consumer)
thread.start()


in_queue.put(object())
print('Producer put 1')
in_queue.put(object())
print('Producer put 2')
in_queue.join()
print('Producer done')
