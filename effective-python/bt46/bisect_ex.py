
import time
import bisect

if __name__ == "__main__":
    x = list(range(10**6))

    start = time.time()
    i = x.index(991234)
    end = time.time()
    print("idx:", i, "  exectime:", end-start,"s")

    start = time.time()
    i = bisect.bisect_left(x, 991234)
    end = time.time()
    print("idx:", i, "  exectime:", end-start,"s")


