# -*- coding: utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()

import asyncio
import requests
import time
from concurrent.futures import ThreadPoolExecutor


def send_request(url): 
    #print('start {}'.format(url))
    response = requests.get(url)
    #time.sleep(2)
    #print('end {}'.format(url))
    #return url
    return response.text


async def send_requests_async(loop, urls):
    '''
    https://stackoverflow.com/questions/22190403/how-could-i-use-requests-in-asyncio/47572164
    run_in_executor는 실제로는 ThreadPoolExecutor를 사용한다.
    그러나 복잡한 처리는 asyncio가 해주기 때문에 속도가 빠르다.
    '''
    #print('future start')
    futures = []
    for url in urls:
        futures.append(loop.run_in_executor(None, send_request, url))

    results = []
    for future in futures:
        results.append(await future)

    return results


def run_in_async(urls):
    # BEST PERFORMANCE AND MEMORY USE
    # 내부적으로는 ThreadPoolExecutor로 실행되는데도 성능은 좋은 편임
    # asyncio에서 async적으로 복잡한 처리를 해주기 때문인듯
    # 메모리 상용량은 run_in_thread_pool 보다 작음
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(send_requests_async(loop, urls))
    loop.close()
    return results


def run_in_thread_pool(urls):
    # max_workers에 따라 성능이 바뀜. 이 케이스는 최소 url 개수 만큼 workers를 지정해줄 필요가 있음
    # 평균 성능은 run_in_async보다 떨어짐.
    # pool 개수에 따라 메모리 사용량이 늘어남. 성능도 달라짐 (당연하지만...)
    results = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        for result in executor.map(send_request, urls):
            results.append(result)

    return results


def run_in_sync(urls):
    results = []
    for url in urls:
        results.append(send_request(url))
    return results

def run_in_gevent(urls):
    # monkey patch를 한경우 전체 사용 메모리 양이 조금 늘어남. 
    #(기본적으로 main thread에 필요한 메모리양인듯)
    # 성능은 run_in_async보다 높다고 볼 수도 없다.

    threads = []
    for url in urls:
        threads.append(gevent.spawn(send_request, url))
    gevent.joinall(threads)

    return [thread.value for thread in threads]

if __name__ == '__main__':
    url1 = 'https://en.wikipedia.org/wiki/Computation'
    url2 = 'https://en.wikipedia.org/wiki/Future'
    url3 = 'https://en.wikipedia.org/wiki/Love'
    urls = [url1, url2, url3, url1, url2, url3, url1, url2, url3]

    '''
    start = time.time()
    run_in_sync(urls)
    end = time.time()
    print('synchro time spend {}s'.format(end - start))
    '''

    start = time.time()
    results = run_in_async(urls)
    end = time.time()
    print('async (ThreadPoolExecutor) time spend {}s'.format(end - start))
    for result in results:
        print(len(result))

    '''
    start = time.time()
    results = run_in_thread_pool(urls)
    end = time.time()
    print('ThreadPoolExecutor time spend {}s'.format(end - start))
    for result in results:
        print(len(result))
    '''


    start = time.time()
    results = run_in_gevent(urls)
    end = time.time()
    print('gevent time spend {}s'.format(end - start))
    for result in results:
        print(len(result))
