# -*- coding: UTF-8 -*-


# 根据命令行参数设置环境类型
import tornado.options

tornado.options.define('port', default=9000, type=int)
tornado.options.define('env', default='offline', type=str)
tornado.options.define('log_level', default='debug', type=str)
tornado.options.define('log_dir', default='./log', type=str)
tornado.options.define('server_name', default='video_server', type=str)
tornado.options.parse_command_line()

# 获取本机IP
import socket
LOCAL_IP = socket.gethostbyname(socket.gethostname())

"""服务基础配置"""
ServerBaseConfig = {
    'env_type':         tornado.options.options.env,  # 环境类型, online|offline
    'listen_port':      tornado.options.options.port,  # 默认监听端口
    'log_level':        tornado.options.options.log_level,  # 日志级别, debug|info|warning|error
    'log_dir':          tornado.options.options.log_dir,  # 日志目录
    'http_timeout':     1.0,  # http请求的超时时间, 单位s
    'monitor_timeout':  1.0,  # 监控超时时间, 单位s
    'server_name':      tornado.options.options.server_name,     # 服务器名称
    'ip':               LOCAL_IP,    # 本机ip
}


"""阿里云图片服务配置"""
PicConfig = {
    'app_key':      'J0A9BNrnwamiBE9t',
    'app_secret':   'JgDCS20hnGRv1dQ1xvylE29F5p2Q7X',
    'bucket_name':  'yxs-pic',
    'internal_end_point':    'oss-cn-beijing-internal.aliyuncs.com',
    'external_end_point':    'oss-cn-beijing.aliyuncs.com',
}


"""微信小程序配置"""
WXAppConfig = {
    'app_id': 'wxd84c8fafe419cb93',
    'app_secret': '4d7cc0ac11b1183d87416abcc13d133f'
}


if ServerBaseConfig['env_type'] == 'online':
    API_PREFIX_CONFIG = {
        'api_url': 'https://api.hundun.cn/url/',
    }
else:
    API_PREFIX_CONFIG = {
        'api_url': 'https://tapi.hundun.cn/url/',
    }


"""耕耕ACCESS_KEY配置"""
AK_CONFIG = {
    'AccessKey_ID': 'LTAIzLudDX4IXZiJ',
    'AccessKey_Secret': 'IptIn3UtYVNg0S8jKMUqg2jOQELTsy'
}


if ServerBaseConfig['env_type'] == 'online':
    # 短信配置
    SmsConfig = {
        'code_expire': 24*60*60,   # 短信计数有效期（单位秒）
        'limit': 10,        # 有效期内的最大次数
        'sms_pattern': 0,  # 0-云片 1-漫道
    }
else:
    # 短信配置
    SmsConfig = {
        'code_expire': 60,   # 短信计数有效期（单位秒）
        'limit': 3,           # 有效期内的最大次数
        'sms_pattern': 0,    # 0-云片 1-漫道
    }
