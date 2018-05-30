#!/usr/bin/env python
# coding=utf-8

import logging


def get_logger():
    """
    创建日志实例
    """
    logger_ = logging.getLogger('proxy')
    handler = logging.FileHandler(filename='{}.log'.format('proxy'), mode='w')
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                  datefmt='%a, %d %b %Y %H:%M:%S')
    handler.setFormatter(formatter)
    logger_.addHandler(handler)
    logger_.setLevel(logging.INFO)
    return logger_

logger = get_logger()

