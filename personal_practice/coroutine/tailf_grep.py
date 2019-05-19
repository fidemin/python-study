
import time
from coroutine import coroutine, printer

'''
pipelining example of coroutine
'''

def follow(f, target=None):
    # 끝 라인으로 간다.
    f.seek(0, 2)

    while True:
        line = f.readline()

        if not line:
            # 파일에 새로 들어온 내용이 없으면 continue
            time.sleep(0.5)
            continue

        if target:
            yield target.send(line)
        else:
            yield line


@coroutine
def grepper(word, target=None):
    while True:
        line = yield

        if word in line:
            if target:
                yield target.send(line)
            else:
                yield line


if __name__ == "__main__":
    logfile = 'log.txt'

    with open(logfile) as f:
        prn = printer()
        grp = grepper('error', prn)
        follower = follow(f, grp)

        for _ in follower:
            pass
