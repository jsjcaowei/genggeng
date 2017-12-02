# -*- coding: utf-8 -*-

import sys
import os
# 添加第三方包目录到系统路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'util', 'site-packages'))

# from PIL import Image, ImageDraw


from conf.server_conf import ServerBaseConfig
import tornado.ioloop, tornado.httpserver, tornado.web
from tornado.log import access_log, gen_log
from url_route import url_route
from url_route import url_route

reload(sys)
sys.setdefaultencoding('utf-8')


def init_logger(listen_port):
    """初始化日志配置"""
    import logging
    from tornado.log import access_log, gen_log, app_log, LogFormatter
    from cloghandler import ConcurrentRotatingFileHandler

    access_log.propagate = False
    gen_log.propagate = False
    app_log.propagate = False

    fmt = ('%(color)s[%(levelname)1.1s %(asctime)s {listen_port}:%(module)s:%(lineno)d:'
           '%(funcName)s]%(end_color)s %(message)s'.format(listen_port=listen_port))
    formatter = LogFormatter(color=False, datefmt=None, fmt=fmt)

    accessLogHandler = logging.handlers.ConcurrentRotatingFileHandler(
        ServerBaseConfig['log_dir'] + '/access.log',
        maxBytes=512 * 1024 * 1024,
        backupCount=10)
    accessLogHandler.setFormatter(formatter)
    access_log.addHandler(accessLogHandler)

    serverLogHandler = logging.handlers.ConcurrentRotatingFileHandler(
        ServerBaseConfig['log_dir'] + '/server.log',
        maxBytes=128 * 1024 * 1024,
        backupCount=5)
    serverLogHandler.setFormatter(formatter)
    gen_log.addHandler(serverLogHandler)
    app_log.addHandler(serverLogHandler)

    access_log.setLevel(logging.INFO)
    gen_log.setLevel(getattr(logging, ServerBaseConfig['log_level'].upper()))
    app_log.setLevel(getattr(logging, ServerBaseConfig['log_level'].upper()))


def handler_format_access(handler):
    """输出handler的标准日志"""
    log_data = handler.format_log() if hasattr(handler, 'format_log') else ''
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    log_method('status=%d tc=%.2fms method=%s uri=%s remote=%s %s',
               handler.get_status(), 1000.0 * handler.request.request_time(),
               handler.request.method, handler.request.uri, handler.request.remote_ip, log_data)

    # request_monitor(handler)


def request_monitor(handler):
    """接口访问: 500和超时监控记录"""
    # 500监控, time_out监控
    if handler.get_status() >= 500 or handler.request.request_time() > ServerBaseConfig['monitor_timeout']:
        if handler.get_status() >= 500:
            desc = '接口发生500'
            detail = ''
        else:
            desc = '接口处理超时'
            detail = '*耗时: %.3fms' % (1000.0 * handler.request.request_time())

        timestamp = handler.task_node.start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        env_type = '生产环境' if ServerBaseConfig['env_type'] == 'online' else '测试环境'
        message = '[{env_type} 监控告警]\n*服务: {server_name}\n*IP: {ip}:{port}\n*时间: {timestamp}\n*描述: {desc}\n' \
                  '*seq_no: {seq_no}\n*URI: {URI}\n{detail}'.format(
            env_type=env_type, server_name=ServerBaseConfig['server_name'], ip=ServerBaseConfig['ip'],
            port=ServerBaseConfig['listen_port'], timestamp=timestamp, desc=desc, seq_no=handler.task_node.seq_no,
            URI=handler.request.uri, detail=detail)

        redis_key = 'server/warning_message/list'
        # 报警数量小于10个
        if handler.task_node.public_redis.llen(redis_key) < 10:
            handler.task_node.public_redis.lpush(redis_key, message)


def main():
    # 检查日志目录不存在则创建
    import os

    if not os.path.isdir(ServerBaseConfig['log_dir']):
        os.mkdir(ServerBaseConfig['log_dir'])

    # web服务
    app = tornado.web.Application(
        handlers=url_route,
        log_function=handler_format_access)

    # 监听端口
    listen_port = ServerBaseConfig['listen_port']
    init_logger(listen_port=listen_port)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(listen_port)

    gen_log.info('video server start at port: %s, env_type: %s, log_level: %s, log_dir: %s',
                 listen_port, ServerBaseConfig['env_type'],
                 ServerBaseConfig['log_level'], ServerBaseConfig['log_dir'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
