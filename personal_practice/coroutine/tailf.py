
import time

def tail_f(f):
    f.seek(0, 2)

    while True:
        line = f.readline()

        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    logfile = 'log.txt'
    with open(logfile) as f:
        for line in tail_f(f):
            print(line, end="")
