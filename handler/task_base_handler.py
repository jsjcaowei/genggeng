# -*- coding: UTF-8 -*-
"""
description: 请求的handler基类
date: 2016-11-15
"""

import json
import time

from tornado.log import gen_log
import tornado.web, tornado.escape
from conf.db_conf import DbConfig
from conf.redis_conf import RedisConfig
from conf.server_conf import AK_CONFIG
from util.convert_object import ConvertObject
from util.mysql_client import MysqlClient
from util.redis_client import RedisClient
from aliyunsdkcore import client

# API接口
video_db = MysqlClient.new_conn(db_config=DbConfig['video'])

# public redis 的连接
public_redis = RedisClient.new_conn(redis_config=RedisConfig['public'])

# 视频点播的ASSESS_ID 和 视频点播的ASSESS_KEY_SECRET
acs_client = client.AcsClient(AK_CONFIG['AccessKey_ID'], AK_CONFIG['AccessKey_Secret'], 'cn-shanghai',
                              auto_retry=True, max_retry_time=3, timeout=120)


class TaskNode(object):
    """请求任务结点, 包括请求的输入/输出, 以及相关的中间信息
    Attributes:
        seq_no:             @str, 请求的序列号
        common_param:       @dict, 请求的公共参数
        business_param:     @dict, 请求的业务参数
        start_datetime:     @datetime, 请求处理的起始时间戳
        start_timestamp:    @float, 请求处理的起始时间戳
        scan_timestamp:     @float, 统计耗时的计时时间戳, 每次计算耗时后都更新到当前时间点
        timecost_list:      @list, 处理的耗时信息, (str(tc_name), float(tc_val))
        landmarks:          @list, 请求处理过程中重要节点的信息
    Methods:
        set_step_timecost: 添加步骤的耗时, 单位ms
        set_landmark_data: 添加节点信息数据
    """

    def __init__(self):
        self.common_param = {}
        self.business_param = {}
        from datetime import datetime

        self.start_datetime = datetime.now()
        self.start_timestamp = time.time()
        self.seq_no = '{:.6f}'.format(self.start_timestamp)
        self.scan_timestamp = self.start_timestamp
        self.timecost_list = []
        self.landmarks = []
        self.result_info = {'error_no': 0, 'error_msg': 'success'}
        self.json_result = ''
        self.api_db = api_db
        self.public_redis = public_redis
        self.acs_client = acs_client

    def set_step_timecost(self, step_name):
        """添加步骤的耗时, 单位ms"""
        new_timestamp = time.time()
        step_timecost = 1000.0 * (new_timestamp - self.scan_timestamp)
        step_timecost = int(step_timecost * 100) / 100.0  # 耗时保留两位小数
        self.timecost_list.append((step_name, step_timecost))
        self.scan_timestamp = new_timestamp
        return

    def set_landmark_data(self, mark_name, mark_data):
        """添加节点信息数据"""
        self.landmarks.append((mark_name, mark_data))


class TaskBaseHandler(tornado.web.RequestHandler):
    """请求的handler基类"""

    def prepare(self):
        """ 重写父类prepare方法: 构造请求任务结点, 解析公共参数 """
        # 接口允许跨域访问
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')

        self.log_result = False  # 日志中是否输出响应结果包
        self.method = self.request.method.upper()
        self.task_node = TaskNode()
        common_param = self.task_node.common_param
        common_param['user_id'] = self.get_param('user_id')
        common_param['app_role'] = self.get_param('app_role', 'yxs')  # app模式

    def get_param(self, param_name, default_value=''):
        """解析请求的参数"""
        ret_val = default_value
        try:
            ret_val = type(default_value)(self.get_argument(param_name))
        except:
            if self.request.method == 'POST':
                if not hasattr(self, 'json_param'):
                    try:
                        self.json_param = tornado.escape.json_decode(self.request.body)
                    except:
                        pass
                if hasattr(self, 'json_param') and param_name in self.json_param:
                    ret_val = type(default_value)(self.json_param[param_name])

        return ret_val

    def write_result(self):
        """返回结果"""
        result_info = ConvertObject.object_2_dict(self.task_node.result_info)
        self.task_node.json_result = json.dumps(result_info)
        self.task_node.set_step_timecost('pack_res')
        self.write(self.task_node.json_result)

    def format_log(self):
        """handler标准日志的信息"""
        # 输出的结果包
        timecost_list = json.dumps(self.task_node.timecost_list)
        landmarks = ConvertObject.object_2_dict(self.task_node.landmarks)
        landmarks = json.dumps(landmarks)
        result = self.task_node.json_result if self.log_result else '<>'
        log_data = ('seq_no={seq_no} common_param={common_param} business_param={business_param} '
                    'error_no={error_no} error_msg={error_msg} '
                    'timecost_list={timecost_list} landmarks={landmarks} '
                    'res_len={result_len} result={result}'
                    .format(seq_no=self.task_node.seq_no,
                            common_param=json.dumps(self.task_node.common_param),
                            business_param=json.dumps(self.task_node.business_param),
                            error_no=self.task_node.result_info['error_no'],
                            error_msg=self.task_node.result_info['error_msg'],
                            timecost_list=timecost_list, landmarks=landmarks,
                            result_len=len(self.task_node.json_result), result=result))
        return log_data
