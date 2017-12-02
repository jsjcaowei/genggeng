#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/9/9 下午10:41

import requests
import json
from tornado.log import gen_log
from conf.server_conf import ServerBaseConfig


class HttpClient(object):
    """封装的http请求类"""
    def __init__(self):
        pass

    @staticmethod
    def request(task_node, url, params=''):
        """http请求封装"""
        if params:
            response = requests.post(url, data=params, timeout=ServerBaseConfig['http_timeout'], verify=False)
        else:
            response = requests.get(url, timeout=ServerBaseConfig['http_timeout'], verify=False)
        task_node.set_step_timecost(step_name='wx_access_token')

        try:
            data = json.loads(response.content)
        except ValueError:
            data = response.content

        if int(response.status_code) == 200:
            gen_log.info('<seq_no=%s> Http调用接口成功, url=%s', task_node.seq_no, url)
            # gen_log.info('<seq_no=%s> Http调用接口成功, url=%s response=%s', task_node.seq_no, url, str(data))
            return data

        gen_log.error('<seq_no=%s> Http调用接口失败, url=%s error=%s', task_node.seq_no, url, str(data))
        return
