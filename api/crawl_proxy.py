# -*- coding:utf-8 -*-
"""
File Name: crawl_proxy
Version:
Description:
Author: liuxuewen
Date: 2018/5/25 15:26
"""
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import re
from database import RedisClient
from logger import logger
from validator import Validator

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

def redefine_requests(url,headers=headers,timeout=3):
    try:
        res = requests.get(url, headers=headers,timeout=timeout)
        return res
    except:
        return None
all_funcs = list()
def collect_crawl_func(func):
    """
    装饰器，用于收集爬虫函数
    """
    all_funcs.append(func)
    return func


class Crawler(object):

    @staticmethod
    @collect_crawl_func
    def crawl_66ip():
        """
        66ip 代理：http://www.66ip.cn
        """
        url = 'http://www.66ip.cn/nmtq.php?getnum=100&amp;isp=0&amp;anonymoustype=4&amp;start=&amp;ports=&amp;export=&amp;ipaddress=&amp;area=0&amp;proxytype=2&amp;api=66ip'
        res = redefine_requests(url)
        if not res:
            return
        items = re.findall(pattern=r'\d+\.\d+\.\d+\.\d+\:\d+', string=res.text)
        for item in items:
            ip, port = item.split(':')
            RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    @collect_crawl_func
    def crawl_xici():
        """
        西刺代理：http://www.xicidaili.com
        """
        urls = ['http://www.xicidaili.com/nn/',
                'http://www.xicidaili.com/nt/',
                'http://www.xicidaili.com/wn/',
                'http://www.xicidaili.com/wt/'
                ]
        for url in urls:
            for page in range(1, 2):
                res =redefine_requests('{}{}'.format(url, page))
                if not res:
                    continue
                soup = BeautifulSoup(res.text, 'lxml')
                # print(soup)
                # time.sleep(1000)
                items = soup.select('#ip_list .odd')
                for item in items:
                    tds = item.select('td')
                    ip = tds[1].text.strip()
                    port = tds[2].text.strip()
                    RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    @collect_crawl_func
    def crawl_kuaidaili():
        """
        快代理：https://www.kuaidaili.com
        """
        for page in range(1, 6):
            url = "https://www.kuaidaili.com/free/inha/{}/".format(page)
            res = redefine_requests(url)
            if not res:
                continue

            soup = BeautifulSoup(res.text, 'lxml')
            items = soup.select('#list table tbody tr')
            for item in items:
                ip = item.find('td', {'data-title': 'IP'}).text.strip()
                port = item.find('td', {'data-title': 'PORT'}).text.strip()
                RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    @collect_crawl_func
    def crawl_ip3366():
        """
        云代理：http://www.ip3366.net
        """
        for page in range(1, 6):
            url = "http://www.ip3366.net/?stype=1&page={}".format(page)
            res = redefine_requests(url)
            if not res:
                return
            soup = BeautifulSoup(res.text, 'lxml')
            items = soup.select('#list table tbody tr')
            for item in items:
                tds = item.select('td')
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    @collect_crawl_func
    def crawl_data5u():
        """
        无忧代理：http://www.data5u.com/
        """
        urls = ["http://www.data5u.com/free/gwgn/index.shtml",
                'http://www.data5u.com/free/gwpt/index.shtml',
                'http://www.data5u.com/free/gwpt/index.shtml',
                'http://www.data5u.com/free/gwpt/index.shtml',
                'http://www.data5u.com/free/index.shtml'
                ]
        for url in urls:
            res = redefine_requests(url)
            if not res:
                return
            soup = BeautifulSoup(res.text, 'lxml')
            items = soup.find_all('ul', class_='l2')
            for item in items:
                spans = item.find_all('span')
                ip = spans[0].text.strip()
                port = spans[1].text.strip()
                RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    @collect_crawl_func
    def crawl_swei360():
        """
        360 代理：http://www.swei360.com
        """
        for page in range(1, 2):
            for style in [1, 3]:
                print(page,style)
                url = "http://www.swei360.com/free/?stype={}&page={}".format(style, page)
                res = redefine_requests(url,timeout=20)
                if not res:
                    continue
                soup = BeautifulSoup(res.text, 'lxml')
                items = soup.select('#list table tbody tr')
                for item in items:
                    tds = item.select('td')
                    ip = tds[0].text.strip()
                    port = tds[1].text.strip()
                    RedisClient.add_proxy_nofilter(check_str='{}|{}'.format(ip, port))

    @staticmethod
    def run():
        """
        启动收集器
        :return: 
        """
        logger.info('Crawler startting...')
        for func in all_funcs:
            # print(func,type(func))
            func()




def filter_proxy(ip, port):
    proxy = {
        'http': 'http://{}:{}'.format(ip, port),
        'https': 'https://{}:{}'.format(ip, port),
    }
    validate = Validator()
    result = validate.validate_proxy(proxy=proxy)
    # print(result, ip, port)
    if result == 4:
        # 将结果存入redis
        RedisClient.add_proxy(check_str='{}|{}'.format(ip, port), value=result)

#使用多进程
def multiprocess_filter_proxy():
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    print(RedisClient.num_proxy_nofilter())
    for _ in range(RedisClient.num_proxy_nofilter()):
        item = RedisClient.pop_proxy_nofilter()
        ip, port = item.split('|')
        pool.apply_async(filter_proxy, args=(ip, port))
    pool.close()
    pool.join()
    print('over')




if __name__ == '__main__':
    while True:
        begin = time.time()
        #爬取代理
        crawler = Crawler()
        crawler.run()
        end = time.time()
        print('爬取代理用时:{}'.format(end - begin))
        #过滤代理
        multiprocess_filter_proxy()
        print('过滤代理用时:{}'.format(time.time() - end))

