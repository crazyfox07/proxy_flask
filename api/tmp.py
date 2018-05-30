# -*- coding:utf-8 -*-
"""
File Name: tmp
Version:
Description:
Author: liuxuewen
Date: 2018/5/25 15:10
"""
import requests

from api.database import RedisClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}
def get_proxy():
    res = requests.post('http://99.48.58.12:9999')
    proxy = res.json().get('proxy')
    return proxy

def func():
    proxy = get_proxy()
    try:
        res = requests.get('https://www.taobao.com/',headers=headers,proxies=proxy,timeout=3)
        print(proxy,res.status_code)
    except:
        print(proxy,'失效')

def tmp2():
    proxies = RedisClient.get_all_proxies()
    print(proxies)
    print(len(proxies))
    for proxy in proxies:
        try:
            res = requests.get('https://www.taobao.com/', headers=headers, proxies=proxy, timeout=3)
            print(proxy, res.status_code)
        except:
            print(proxy, '失效')


if __name__ == '__main__':
    tmp2()
    # import time
    # start = time.time()
    # for _ in range(100):
    #     func()
    # print('time use:{}'.format(time.time()-start))