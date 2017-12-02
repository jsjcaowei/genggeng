#!/usr/bin/env python
# coding=utf-8


"""对redis访问的封装, 后续要考虑支持主备检测切换"""

import redis


class RedisClient(object):
    @staticmethod
    def new_conn(redis_config):
        _redis_conn = redis.StrictRedis(
            host=redis_config['ip'],
            port=redis_config['port'],
            db=redis_config['db'],
            socket_timeout=1.0
        )
        return _redis_conn
