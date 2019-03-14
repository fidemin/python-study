
import asyncio
import time

strings = ['abc', 'efg', 'hij'] * 10

async def sleep(string):
    await asyncio.sleep(0.5)
    return string + "1"

async def sleep_and_print(string, sem):
    async with sem:
        string = await sleep(string)
        print(string)


if __name__ == "__main__":
    sem = asyncio.Semaphore(5)
    futures = [sleep_and_print(string, sem) for string in strings]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))

