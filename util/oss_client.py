#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/9/9 下午7:51

import oss2
from conf.server_conf import PicConfig


class OSSClient(object):
    """对阿里云oss2操作的封装"""
    app_key = PicConfig['app_key']
    app_secret = PicConfig['app_secret']
    bucket_name = PicConfig['bucket_name']
    internal_end_point = PicConfig['internal_end_point']
    external_end_point = PicConfig['external_end_point']

    pic_auth = oss2.Auth(app_key, app_secret)
    pic_bucket = oss2.Bucket(pic_auth, internal_end_point, bucket_name)

    @staticmethod
    def upload_image(upload_name, f):
        """上传文件到oss"""
        result = OSSClient.pic_bucket.put_object(upload_name, f)
        if result.status != 200:
            return ''
        else:
            oss_url = 'http://%s.%s/%s' % (OSSClient.bucket_name, OSSClient.external_end_point, upload_name)
            return oss_url
