#!/usr/bin/env python
# coding=utf-8


"""对mysql访问的封装, 后续要考虑支持主备检测切换"""

import util.torndb


class MysqlClient(object):
    @staticmethod
    def new_conn(db_config):
        _db_conn = util.torndb.Connection(
            host=db_config['host'],
            database=db_config['name'],
            user='dever',
            password='dever',
            charset='utf8mb4'
        )
        return _db_conn
