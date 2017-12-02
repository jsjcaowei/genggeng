# -*- coding: utf-8 -*-

"""
微信相关的处理model
"""

from base_model import *
from conf.server_conf import WXAppConfig


class WXAccessToken(object):
    """微信access token结构"""
    def __init__(self):
        self.access_token = ''   # access token, @str
        self.expires_in = ''     # 多久过期, 单位: 秒 @int


class WXModel(BaseModel):
    """ wx model类
    Methods:
    """
    def __init__(self):
        super(WXModel, self).__init__()

    @staticmethod
    def get_access_token(task_node, refresh=0):
        """获取公众平台的API调用所需的access_token"""
        redis_key = 'public/global/wx_access_token'
        token_info = WXAccessToken()

        token_info.access_token = task_node.public_redis.get(redis_key)
        task_node.set_step_timecost(step_name='public_redis')
        if token_info.access_token and refresh == 0:
            token_info.expires_in = task_node.public_redis.ttl(redis_key)
            gen_log.info('<seq_no=%s> 从redis获取微信access_token成功, access_token=%s expires_in=%s', task_node.seq_no,
                token_info.access_token, token_info.expires_in)
            return token_info

        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            WXAppConfig['app_id'], WXAppConfig['app_secret'])
        response = HttpClient.request(task_node, url)
        if response and 'errcode' not in response:      # 有errcode说明发生了错误
            token_info.access_token = response.get('access_token')
            token_info.expires_in = response.get('expires_in')
            task_node.public_redis.set(redis_key, response.get('access_token'))     # 更新到redis
            task_node.public_redis.expire(redis_key, response.get('expires_in'))
            gen_log.info('<seq_no=%s> 获取wx access token成功, token_info=%s', task_node.seq_no, str(response))
            return token_info
        gen_log.error('<seq_no=%s> 获取wx access token失败, token_info=%s', task_node.seq_no, str(response))
        return

    @staticmethod
    def get_wxacode_image(task_node, params):
        """获取小程序码图片链接"""
        refresh = 0
        for _ in range(2):
            token_info = WXModel.get_access_token(task_node, refresh)
            if not token_info:
                gen_log.error('<seq_no=%s> 获取微信access token失败', task_node.seq_no)
                task_node.result_info['error_no'] = 1
                task_node.result_info['error_msg'] = '获取微信access token失败'
                return
            access_token = token_info.access_token
            url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s' % access_token
            response = HttpClient.request(task_node, url, json.dumps(params))
            if response and 'errcode' not in response:      # 有errcode说明发生了错误
                gen_log.info('<seq_no=%s> 获取小程序码图片成功', task_node.seq_no)
                return response
            # 调用接口失败, 尝试强制刷新access token重试一次
            refresh = 1

        gen_log.error('<seq_no=%s> 获取小程序码图片失败', task_node.seq_no)
        return
