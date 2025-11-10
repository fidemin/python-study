import asyncio
from contextlib import asynccontextmanager


def download_webpage(url):
    print(f"Downloading {url} ...")
    import time

    time.sleep(1)
    return f"<html>{url}</html>"


def update_stats(url):
    print(f"Updating stats for {url} ...")
    import time

    time.sleep(0.5)


def process(data):
    print("Processing data:", data[:30], "...")


@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_running_loop()
    # to use blocking code in async context, use run_in_executor
    data = await loop.run_in_executor(None, download_webpage, url)
    try:
        yield data
    finally:
        # to use blocking code in async context, use run_in_executor
        await loop.run_in_executor(None, update_stats, url)


async def main():
    async with web_page("google.com") as data:
        process(data)


if __name__ == "__main__":
    asyncio.run(main())
