
def safe_division(dividend, divisor, *, ignore_overflow=False, ignore_zero_division=False):
    try:
        return dividend / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


print(safe_division(12, 0, ignore_zero_division=True)) 
