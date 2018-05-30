# -*- coding:utf-8 -*-
"""
File Name: validator
Version:
Description:
Author: liuxuewen
Date: 2018/5/25 15:45
"""

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}
class Validator(object):

    def __init__(self):
        self. headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        }
        #验证网站
        self.validate_urls = [
            r'https://www.baidu.com/',#百度
            r'http://www.sina.com.cn/',#新浪网
            r'https://www.taobao.com/',#淘宝
            r'https://httpbin.org/'

        ]
        self.result = 0

    #验证
    def validate_proxy(self,proxy):
        for url in self.validate_urls:
            try:
                res = requests.get(url,headers=headers,proxies=proxy,timeout=3)
                if res.status_code == 200:
                    self.result += 1
                else:
                    break
            except:
                break
        return self.result


if __name__ == '__main__':
    ip, port = '139.224.80.139 3128'.split(' ')
    proxy = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'https://{}:{}'.format(ip, port),
    }
    for i in range(100):
        print(i)
        validate = Validator()
        print(validate.validate_proxy(proxy))




