from time import time
from concurrent.futures import ProcessPoolExecutor


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


if __name__ == '__main__':
    numbers = [
        (1963309, 2265939), (2042948, 23894729),
        (23892429, 28394279), (2183914, 2839123),
        (23892429, 28394279)
    ]

    start = time()
    results = list(map(gcd, numbers))
    end = time()
    print('normal: Took {:.3f} seconds'.format(end-start))
    print('results: ', results)

    start = time()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, numbers))
    end = time()
    print('ProcessPoolExecutor: Took {:.3f} seconds'.format(end-start))
    print('results: ', results)

