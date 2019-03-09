
import gevent
from gevent import monkey
from gevent.lock import Semaphore
from urllib.request import urlopen

monkey.patch_all()
urls = ['https://google.com', 'https://magictbl.com', 'https://naver.com'] * 10

def print_head(url, sem):
    with sem:
        print('Starting {}'.format(url))
        data = urlopen(url).read()
        print('{}: {} bytes'.format(url, len(data)))
        return 1


if __name__ == "__main__":
    sem = Semaphore(10)
    jobs = [gevent.spawn(print_head, url, sem) for url in urls]
    print("-- start --")
    greenlets = gevent.wait(jobs)
