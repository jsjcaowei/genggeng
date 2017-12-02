#!/usr/bin/env python
#coding=utf-8

"""
description: 手机短信的数据管理
date: 2017-01-16
"""

import urllib
from tornado.httpclient import AsyncHTTPClient
from tornado.log import gen_log
import json
from conf.server_conf import SmsConfig
import httplib

class SmsModel(object):
    """手机短信息的数据管理
    Methods:
        send_sms: 给指定手机号码发送短信
        is_valid_phone: 是否为合法的手机号码
        __is_china_phone: 是否为国内手机号码格式
        __is_i18n_phone: 是否为国际手机号码格式
        __send_china_sms: 发送国内手机短信
        __send_i18n_sms: 发送国际手机短信
    """

    """云片短信模块"""
    # 服务地址
    yupian_sms_host = "sms.yunpian.com"
    # 端口号
    yupian_port = 443
    # 版本号
    yupian_version = "v2"
    # 成功注册后登录云片官网,进入后台可查看
    yupian_APIKEY = 'cc237a970437a946c2a07e5ac69005db'

    @staticmethod
    def send_sms(phone, sms_text):
        """给指定手机号码发送短信
        Args:
            phone:      @str, 接收短信的手机号
            sms_text:   @str, 短信内容, 不包括公司签名
        Return:
            -1:     手机号码不合法
            -2:     短信发送提交失败
            0:      短信发送提交成功
        """
        # 判断手机格式
        is_china = SmsModel.__is_china_phone(phone=phone)
        is_i18n = SmsModel.__is_i18n_phone(phone=phone)
        if not is_china and not is_i18n:
            gen_log.info('输入手机号码格式不合法, phone=%s', phone)
            return -1

        if is_china and SmsConfig['sms_pattern'] == 0 and '验证码' in sms_text:
            # 国内+验证码+云片模式
            sms_text = '【耕耕科技】{}'.format(sms_text)
            SmsModel._yunpian_send_sms_async(phone=phone, sms_text=sms_text)
            return 0
        else:
            # 给短信内容添加公司签名并发送
            sms_text = '{}【耕耕科技】'.format(sms_text)
            # 以异步方式发送短信
            if is_china and SmsModel.__send_china_sms_async(phone=phone, sms_text=sms_text):
                return 0  # 国内短信提交成功
            if is_i18n and SmsModel.__send_i18n_sms_async(phone=phone, sms_text=sms_text):
                return 0  # 国际短信提交成功

        return -2  # 短信提交失败

    @staticmethod
    def is_valid_phone(phone):
        """是否为合法的手机号码"""
        if SmsModel.__is_china_phone(phone) or SmsModel.__is_i18n_phone(phone):
            return True
        return False

    @staticmethod
    def __is_china_phone(phone):
        """是否为国内手机号码格式"""
        import re
        return bool(re.match('^1[0-9]{10}$', str(phone)))

    @staticmethod
    def __is_i18n_phone(phone):
        """是否为国际手机号码格式"""
        import re
        return bool(re.match('^00[0-9]{10,}$', str(phone)))

    @staticmethod
    def __send_china_sms(phone, sms_text):
        """发送国内手机短信"""
        import requests
        api_url = 'http://sdk.entinfo.cn:8061/mdsmssend.ashx'
        post_param = {
            'sn': 'SDK-BBX-010-23834',
            'pwd': 'B682DED47EFA477AA33E6D9305290D0D',
            'mobile': phone,
            'content': sms_text,
        }
        try:
            sms_request = requests.post(api_url, data=post_param, timeout=1.0)
        except Exception, e:
            gen_log.error('国内短信发送接口抛出异常, phone=%s sms_text=%s exception=%s',
                phone, sms_text, str(e))
            return False
        if sms_request.text.startswith('-'):
            gen_log.error('国内短信发送接口返回失败, phone=%s sms_text=%s response=%s',
                phone, sms_text, sms_request.text)
            return False
        gen_log.debug('国内短信发送接口提交成功, phone=%s sms_text=%s response=%s',
            phone, sms_text, sms_request.text)
        return True

    @staticmethod
    def __send_i18n_sms(phone, sms_text):
        """发送国际手机短信"""
        import requests
        api_url = 'http://sdk.entinfo.cn:8060/gjWebService.asmx/mdSmsSend_g'
        post_param = {
            'sn': 'SDK-BBX-010-25730',
            'pwd': '3BE95520F8EF57FCAE6F7CDE9AEB1DC2',
            'mobile': phone,
            'content': sms_text,
            'ext': '',
            'stime': '',
            'rrid': '',
        }
        try:
            sms_request = requests.post(api_url, data=post_param, timeout=1.0)
        except Exception, e:
            gen_log.error('国际短信发送接口抛出异常, phone=%s sms_text=%s exception=%s',
                phone, sms_text, str(e))
            return False
        import re
        sms_response = re.sub('<[^>]+>', '', sms_request.text)
        if sms_response.strip().startswith('-'):
            gen_log.error('国际短信发送接口返回失败, phone=%s sms_text=%s response=%s',
                phone, sms_text, sms_request.text)
            return False
        gen_log.debug('国际短信发送接口提交成功, phone=%s sms_text=%s response=%s',
            phone, sms_text, sms_request.text)
        return True

    @staticmethod
    def __send_china_sms_async(phone, sms_text):
        """异步发送国内手机短信"""
        api_url = 'http://sdk.entinfo.cn:8061/mdsmssend.ashx'
        post_param = {
            'sn': 'SDK-BBX-010-23834',
            'pwd': 'B682DED47EFA477AA33E6D9305290D0D',
            'mobile': phone,
            'content': sms_text,
        }

        http_client = AsyncHTTPClient()
        http_client.fetch(api_url, method='POST', body=urllib.urlencode(post_param))
        gen_log.debug('国内短信发送接口提交, phone=%s sms_text=%s', phone, sms_text)
        return True

    @staticmethod
    def __send_i18n_sms_async(phone, sms_text):
        """发送国际手机短信"""
        api_url = 'http://sdk.entinfo.cn:8060/gjWebService.asmx/mdSmsSend_g'
        post_param = {
            'sn': 'SDK-BBX-010-25730',
            'pwd': '3BE95520F8EF57FCAE6F7CDE9AEB1DC2',
            'mobile': phone,
            'content': sms_text,
            'ext': '',
            'stime': '',
            'rrid': '',
        }

        http_client = AsyncHTTPClient()
        http_client.fetch(api_url, method='POST', body=urllib.urlencode(post_param))
        gen_log.debug('国际短信发送接口提交成功, phone=%s sms_text=%s', phone, sms_text)
        return True

    @staticmethod
    def yunpian_send_voice(phone, code):
        """给指定手机号码发送语音
        Args:
            code:       @str,
            phone:      @str, 接收短信的手机号
        Return:
            -1:     手机号码不合法
            -2:     短信发送提交失败
            0:      短信发送提交成功
        """
        # 判断手机格式
        is_china = SmsModel.__is_china_phone(phone=phone)
        if not is_china:
            gen_log.info('非国内手机号码, phone=%s', phone)
            return -1

        # 语音短信 and vertify code
        if is_china and SmsModel._yunpian_send_china_voice(phone=phone, code=code):
            return 0  # 国内短信提交成功
        return -2  # 短信提交失败

    @staticmethod
    def _yunpian_send_china_voice(phone, code):
        """
        :param phone: 手机号码
        :param code: 验证码
        :return:
        """

        # 智能匹配模板短信接口的URI
        sms_send_uri = "/" + SmsModel.yupian_version + "/voice/send.json"
        params = urllib.urlencode({
            'apikey': SmsModel.yupian_APIKEY,
            'code': code,
            'mobile': phone
            })
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPSConnection(SmsModel.yupian_sms_host, port=SmsModel.yupian_port, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        gen_log.debug('语音短信发送接口返回 phone=%s code=%s response=%s',
                      phone, code, response_str)
        if json.loads(response_str)['count'] > 0:
            return False
        return True

    @staticmethod
    def _yunpian_send_sms_async(phone, sms_text):
        """
            云片异步智能匹配模板
        :param text: 需要使用已审核通过的模板或者默认模板
        :param mobile: 接收的手机号,仅支持单号码发送
        :return:
        """
        # 智能匹配模板短信接口的URI
        sms_send_uri = "/" + SmsModel.yupian_version + "/sms/single_send.json"
        params = urllib.urlencode({'apikey': SmsModel.yupian_APIKEY, 'text': sms_text, 'mobile': phone})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        http_client = AsyncHTTPClient()
        http_client.fetch('http://{}{}'.format(SmsModel.yupian_sms_host, sms_send_uri), method='POST', headers = headers,  body=params)
        gen_log.debug('国际短信发送接口提交成功, phone=%s sms_text=%s', phone, sms_text)
        return True