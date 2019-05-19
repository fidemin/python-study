
from functools import wraps
from time import time

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        return_value = func(*args, **kwargs)
        msg = 'Executing {} took {:.03} seconds.'.format(func.__name__, time() - start)
        print(msg)
        return return_value
    return wrapper


def fib(n):
    return fib(n - 1) + fib(n - 2) if n > 1 else n


# 데코레이터를 쓰면 재귀 방식이라 log_execution_time이 여러번 호출된다.
timed_fib = log_execution_time(fib)
