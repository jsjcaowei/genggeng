# -*- coding: UTF-8 -*-

"""redis的相关配置"""
from conf.server_conf import ServerBaseConfig


if ServerBaseConfig['env_type'] == 'online':

    RedisConfig = {
        # 公共redis
        'public': {
            'ip': '10.172.138.126',
            'port': 19736,
            'db':   0,
        },
    }

else:

    RedisConfig = {
        # 公共redis
        'public': {
            'ip':   '10.172.162.76',
            'port': 19736,
            'db':   4,
        },
    }
