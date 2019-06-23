import asyncio
import requests
import time

def send_request(url): 
    #print('start {}'.format(url))
    response = requests.get(url)
    #print('end {}'.format(url))
    return response.text

async def example(loop, urls, result):
    #print('future start')
    future1 = loop.run_in_executor(None, send_request, urls[0])
    future2 = loop.run_in_executor(None, send_request, urls[1])
    future3 = loop.run_in_executor(None, send_request, urls[2])
    #print('future end')
    #print('response1 start')
    response1 = await future1
    #print('response1 end')
    #print('response2 start')
    response2 = await future2
    #print('response2 end')
    #print('response3 start')
    response3 = await future3
    #print('response3 end')
    result.extend([response1, response2, response3])

if __name__ == '__main__':
    url1 = 'https://en.wikipedia.org/wiki/Computation'
    url2 = 'https://en.wikipedia.org/wiki/Future'
    url3 = 'https://en.wikipedia.org/wiki/Love'
    urls = [url1, url2, url3]
    start = time.time()
    loop = asyncio.get_event_loop()
    results = []
    loop.run_until_complete(example(loop, urls, results))
    loop.close()
    end = time.time()
    print('time spend {}s'.format(end - start))

    for result in results:
        print(len(result))

    start = time.time()
    results = []
    for url in urls:
        results.append(send_request(url))
    end = time.time()
    print('time spend {}s'.format(end - start))

