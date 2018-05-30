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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

def remove_ineffective_proxy():
    """
    定期验证代理是否还有效，删除失效的代理
    :return: 
    """
    validate_urls = [
        r'https://www.baidu.com/',  # 百度
        r'http://www.sina.com.cn/',  # 新浪网
        r'https://www.taobao.com/',  # 淘宝
        r'https://httpbin.org/',
    ]
    while True:
        url = random.choice(validate_urls)
        proxy = RedisClient.get_proxy().get('proxy')
        if proxy:
            try:
                res = requests.get(url,headers=headers,proxies=proxy,timeout=3)
                # print(proxy)
            except:

                host,port = re.findall(r'//(.+):(\d+)',proxy['http'])[0]
                # print(host,port)
                check_str = '{}|{}'.format(host,port)
                RedisClient.remove_proxy(check_str)
        time.sleep(2)

if __name__ == '__main__':
    remove_ineffective_proxy()