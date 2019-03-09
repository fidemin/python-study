
import asyncio
import aiohttp

urls = ['https://google.com', 'https://magictbl.com', 'https://naver.com'] * 10


async def call_url(url, sem):
    async with sem:
        print('Starting {}'.format(url))
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            data = await response.text()
            print('{}: {} bytes'.format(url, len(data)))
            return data


if __name__ == "__main__":
    sem = asyncio.Semaphore(5)
    futures = [call_url(url, sem) for url in urls]
    loop = asyncio.get_event_loop()
    print("-------- start --------")
    loop.run_until_complete(asyncio.wait(futures))
    print("----- the end --------")

