
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s : %s' % (message, values_str))

def log_args(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s : %s' % (message, values_str))

log('My number is', [1, 2])
log('Hello', [])

log_args('My number is', 1, 2)
log_args('Hello')
