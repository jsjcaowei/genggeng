# -*- coding: utf-8 -*-

from base_service import *
from model.wx_model import WXModel
from model.video_model import  VideoModel


class VideoService(BaseService):
    """
    视频服务类
    Methods:
    """
    def __init__(self):
        super(VideoService, self).__init__()

    @staticmethod
    def get_play_video_upload_auth(task_node):
        """获取公众平台的API调用所需的access_token"""
        result_info = task_node.result_info
        video_title = task_node.business_param.get('video_title', '')
        video_file_name = task_node.business_param.get('video_title', '')
        video_size = task_node.business_param.get('video_file_name', '')
        video_description = task_node.business_param.get('video_description', '')
        video_cover_url = task_node.business_param.get('video_cover_url', '')

        # 获取access token info
        token_info = VideoModel.create_upload_video(task_node, video_title, video_file_name, video_size,
                                                    video_description, video_cover_url)
        if token_info:
            result_info['data'] = token_info
        else:
            gen_log.error('<seq_no=%s> 获取微信access token失败', task_node.seq_no)
            task_node.result_info['error_no'] = 1
            task_node.result_info['error_msg'] = '获取微信access token失败'
        return

    @staticmethod
    def get_video_play_auth(task_node):
        """获取小程序码图片链接"""
        result_info = task_node.result_info
        video_id = task_node.business_param['video_id']

        if not video_id:
            gen_log.error('<seq_no=%s> 获取视频播放凭证失败, video_id=%s', task_node.seq_no, video_id)
            result_info['error_no'] = -1
            result_info['error_msg'] = '获取视频播放凭证失败'
            return

        response = VideoModel.get_video_play_auth_info(task_node, wxa_key)
        playauth = response.get('PlayAuth')
        task_node.result_info['data'] = {'play_auth': playauth, 'video_id': video_id}
        gen_log.info('<seq_no=%s> 获取视频播放凭证ok, video_id=%s', task_node.seq_no, video_id)

        return

    @staticmethod
    def get_video_play_url(task_node):
        """获取小程序码图片链接"""
        result_info = task_node.result_info
        video_id = task_node.business_param['video_id']

        if not video_id:
            gen_log.error('<seq_no=%s> 获取视频播放凭证失败, video_id=%s', task_node.seq_no, video_id)
            result_info['error_no'] = -1
            result_info['error_msg'] = '获取视频播放凭证失败'
            return

        response = VideoModel.get_play_address_info(task_node)
        playauth = response.get('PlayAuth')
        task_node.result_info['data'] = {'play_auth': playauth, 'video_id': video_id}
        gen_log.info('<seq_no=%s> 获取视频播放凭证ok, video_id=%s', task_node.seq_no, video_id)

        return

