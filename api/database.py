# -*- coding:utf-8 -*-
"""
File Name: database
Version:
Description:
Author: liuxuewen
Date: 2018/5/25 14:15
"""
import configparser
import os
import redis
import random


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config'))
redis_section = 'redis_section'
redis_host = config.get(section=redis_section,option='REDIS_HOST')
redis_port = config.getint(section=redis_section,option='REDIS_PORT')
redis_password = config.get(section=redis_section,option='PASSWORD')
redis_db = config.getint(section=redis_section,option='DB')
redis_key_expire = config.getint(section=redis_section,option='KEY_EXPIRE')
redis_set_name = config.get(section=redis_section,option='SET_NAME')


class RedisClient(object):
    #连接redis数据库
    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    r = redis.StrictRedis(connection_pool=pool)

    def __init__(self):
        pass
    @classmethod
    def remove_proxy(cls,check_str):
        cls.r.delete(check_str)

    @classmethod
    def get_all_proxies(cls):
        items_all = cls.r.keys()
        results = list()
        if b'proxy_nofilter' in items_all:
            items_all.remove(b'proxy_nofilter')
        for item in items_all:
            item = item.decode(encoding='utf8')
            host, port = item.split('|')
            proxy_chosen = {
                'http': 'http://{}:{}'.format(host, port),
                'https': 'https://{}:{}'.format(host, port)
            }
            results.append(proxy_chosen)
        return results

    @classmethod
    def get_proxy(cls):
        """        
        :param proxy_num: 需要返回的代理数目
        :return: 
        """
        items_all = cls.r.keys()
        if b'proxy_nofilter' in items_all:
            items_all.remove(b'proxy_nofilter')
        if not items_all:
            return {'available':False}
        proxy_random = random.choice(items_all).decode(encoding='utf8')

        host,port = proxy_random.split('|')
        proxy_chosen = {
            'http':'http://{}:{}'.format(host,port),
            'https': 'https://{}:{}'.format(host, port)
        }
        return {'available':True,'proxy':proxy_chosen}

    # 将过滤后的proxy加入到redis数据库
    @classmethod
    def add_proxy(cls,check_str, value):
        if check_str not in cls.r.keys():
            cls.r.set(check_str, value)
            # 设置key的失效时间
            # cls.r.expire(check_str, redis_key_expire)

    # 将未被过滤的proxy加入到redis数据库的集合中
    @classmethod
    def add_proxy_nofilter(cls, check_str):
        cls.r.sadd(redis_set_name,check_str)

    #从未被过滤的proxy集合中取一个proxy
    @classmethod
    def pop_proxy_nofilter(cls):
        proxy = cls.r.spop(redis_set_name)
        proxy = proxy.decode(encoding='utf8')
        return proxy

    #返回未被过滤的proxy集合的元素数目
    @classmethod
    def num_proxy_nofilter(cls):
        num = cls.r.scard(redis_set_name)
        return num


if __name__ == '__main__':
     a  = RedisClient.get_proxy()
     print(a)
    # for _ in range(20):
    #     proies = RedisClient.pop_proxy_nofilter()
    #     print(proies)
