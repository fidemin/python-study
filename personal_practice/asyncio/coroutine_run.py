import asyncio


class Step:
    def __await__(self):
        # Suspend once, then resume
        print("  [Step.__await__] suspending...")
        yield
        print("  [Step.__await__] resuming...")
        return


async def f():
    try:
        while True:
            await Step()
    except asyncio.CancelledError:
        print("Coroutine was cancelled")


if __name__ == "__main__":
    coro = f()

    while True:
        input_ = input(">> ")
        if input_ == "send":
            coro.send(None)
        elif input_ == "cancel":
            try:
                coro.throw(asyncio.CancelledError)
            except StopIteration:
                print("Coroutine has exited after cancellation")
                break
        else:
            coro.throw(Exception(f"Unknown command: {input_}"))
