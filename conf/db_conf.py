# -*- coding: UTF-8 -*-

"""数据库的相关配置"""
from conf.server_conf import ServerBaseConfig

if ServerBaseConfig['env_type'] == 'online':

    DbConfig = {
        # 用户数据库
        'user': {
            'host': '172.17.47.106:3306',
            'name': 'user',
        },
        # 视频数据库
        'video': {
            'host': '172.17.47.106:3306',
            'name': 'video',
        }
    }

else:

    DbConfig = {
        # 用户数据库
        'user': {
            'host': '172.17.47.106:3306',
            'name': 'user',
        },
        'video': {
            'host': '172.17.47.106:3306',
            'name': 'video',
        }
    }
