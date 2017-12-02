#! /usr/bin/env python
# -*- coding: utf-8 -*-


from base_service import *
from model.video_model import UrlModel


class UrlService(BaseService):
    """链接处理服务类
    Methods:
    """
    def __init__(self):
        super(UrlService, self).__init__()

    @staticmethod
    def get_qrcode_image(task_node, http_url):
        """获取给定http链接的二维码图片链接"""
        result_info = task_node.result_info
        result_data = result_info['data'] = {}

        # 先转短连接
        short_url = UrlModel.generate_short_url(task_node, http_url)

        # 是否已经生成过url的二维码图片
        qrcode_image = UrlModel.get_qrcode_image(task_node, short_url)
        if qrcode_image:
            result_data['qrcode_image'] = qrcode_image
            return

        # 生成二维码图片
        image = UrlModel.generate_qrcode(short_url)
        sf = StringIO.StringIO()  # string io对象
        image.save(sf)
        sf.seek(0)

        # 上传到阿里云图片服务器
        upload_name = hashlib.md5(str(time.time()) + short_url).hexdigest()
        qrcode_image = OSSClient.upload_image(upload_name, sf)
        task_node.set_step_timecost(step_name='upload_image')

        if not qrcode_image:
            gen_log.error('<seq_no=%s> 生成二维码图片链接失败, http_url=%s', task_node.seq_no, http_url)
            task_node.result_info['error_no'] = 1
            task_node.result_info['error_msg'] = '生成二维码图片链接失败'
            return

        # 将生成的链接入库
        UrlModel.add_qrcode_image(task_node, short_url, qrcode_image)

        gen_log.info('<seq_no=%s> 获取二维码图片链接成功, http_url=%s', task_node.seq_no, http_url)
        result_data['qrcode_image'] = qrcode_image
        return
