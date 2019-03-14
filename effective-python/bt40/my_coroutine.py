
def my_coroutine():
    while True:
        received = yield
        print('Received:', received)


it = my_coroutine()
next(it)
it.send('First')
it.send('Second')
