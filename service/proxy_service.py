# -*- coding:utf-8 -*-
"""
File Name: proxy_service
Version:
Description:
Author: liuxuewen
Date: 2018/5/30 11:22
"""
from flask_restful import Resource


from api.database import RedisClient


class FecthProxy(Resource):
    def get(self):
        return {'result':'ok'}

    def post(self):
        proxies = RedisClient.get_proxy()
        return proxies

