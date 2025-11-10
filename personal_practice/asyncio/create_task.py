import asyncio


async def f():
    print("Task started")
    await asyncio.sleep(1.0)
    print("Task completed")
    return "Result"


async def main():
    for i in range(10):
        task = asyncio.create_task(f())
        print(f"Iteration {i}")


if __name__ == "__main__":
    asyncio.run(main())
