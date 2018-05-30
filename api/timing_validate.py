# -*- coding:utf-8 -*-
"""
File Name: timing_validate
Version:
Description:
Author: liuxuewen
Date: 2018/5/30 13:41
"""
import requests
from database import RedisClient
import re
import time
import random
import multiprocessing


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

validate_urls = [
    r'https://www.baidu.com/',  # 百度
    r'http://www.sina.com.cn/',  # 新浪网
    r'https://www.taobao.com/',  # 淘宝
    r'https://httpbin.org/',
]

def remove_ineffective_proxy(proxy):
    url = random.choice(validate_urls)
    try:
        res = requests.get(url, headers=headers, proxies=proxy, timeout=3)
        print(proxy, 'ok')
    except:
        host, port = re.findall(r'//(.+):(\d+)', proxy['http'])[0]
        check_str = '{}|{}'.format(host, port)
        RedisClient.remove_proxy(check_str)
        print(proxy, 'fail')

def run():
    """
    定期验证代理是否还有效，删除失效的代理
    :return: 
    """
    while True:
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        proxies = RedisClient.get_all_proxies()
        print(len(proxies))
        for proxy in proxies:
            pool.apply_async(remove_ineffective_proxy,args=(proxy,))
        pool.close()
        pool.join()
        time.sleep(10)

if __name__ == '__main__':
    run()