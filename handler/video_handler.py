# -*- coding: UTF-8 -*-
"""
微信调用相关的处理
"""
from tornado.log import gen_log

from handler.task_base_handler import TaskBaseHandler
from service.video_service import VideoService


class GetVideoUploadHandler(TaskBaseHandler):
    """获取公众平台的API调用所需的access_token
    Uri: /video/save_video_info
    Args:
        refresh:       @str, 是否强制刷新, 1: 强制刷新, 0: 不强制刷新
    """
    def get(self):
        self.task_node.business_param['video_title'] = self.get_param('video_title', '')
        self.task_node.business_param['video_file_name'] = self.get_param('video_file_name', '')
        self.task_node.business_param['video_size'] = self.get_param('video_size', '')
        self.task_node.business_param['video_description'] = self.get_param('video_description', '')
        self.task_node.business_param['video_cover_url'] = self.get_param('video_cover_url', '')

        if not self.task_node.business_param['video_size'].isdigit():
            gen_log.error('<seq_no=%s> 请求参数不合法, refresh%s', self.task_node.seq_no, self.task_node.business_param['video_size'])
            self.task_node.result_info['error_no'] = 1
            self.task_node.result_info['error_msg'] = '请求参数不合法'
            super(GetVideoUploadHandler, self).write_result()
            return

        VideoService.get_play_video_upload_auth(self.task_node)
        super(GetVideoUploadHandler, self).write_result()

    def get(self):
        self.post()


class GetVideoPlayAuthHandler(TaskBaseHandler):
    """
    获取视频播放相关信息
    Uri: /video/get_video_play_i
    Args:
        video_id:      @str, video_id
        user_id:       @str, 用户id
    """
    def get(self):
        video_id = self.task_node.business_param['video_id'] = self.get_param('video_id')
        # 参数校验
        if video_id:
            VideoService.get_video_play_info(self.task_node)
        else:
            gen_log.error('<seq_no=%s> 请求参数不合法, video_id=%s', self.task_node.seq_no, video_id)
            self.task_node.result_info['error_no'] = 1
            self.task_node.result_info['error_msg'] = '请求参数不合法'
        super(GetVideoPlayAuthHandler, self).write_result()



class GetVideoPlayUrlHandler(TaskBaseHandler):
    """
    获取视频播放相关信息
    Uri: /video/get_video_play_url
    Args:
        video_id:      @str, video_id
        user_id:       @str, 用户id
    """
    def get(self):
        video_id = self.task_node.business_param['video_id'] = self.get_param('video_id')
        # 参数校验
        if video_id:
            VideoService.get_video_play_url(self.task_node)
        else:
            gen_log.error('<seq_no=%s> 请求参数不合法, video_id=%s', self.task_node.seq_no, video_id)
            self.task_node.result_info['error_no'] = 1
            self.task_node.result_info['error_msg'] = '请求参数不合法'
        super(GetVideoPlayUrlHandler, self).write_result()


class GetVideoPlayUrlHandler(TaskBaseHandler):
    """
    获取视频播放相关信息
    Uri: /video/get_video_play_url
    Args:
        video_id:      @str, video_id
        user_id:       @str, 用户id
    """
    def post(self):
        video_id = self.task_node.business_param['ali_vod_id'] = self.get_param('ali_vod_id')
        video_id = self.task_node.business_param['ali_vod_id'] = self.get_param('ali_vod_id')
        # 参数校验
        if video_id:
            VideoService.save_video_info(self.task_node)
        else:
            gen_log.error('<seq_no=%s> 请求参数不合法, video_id=%s', self.task_node.seq_no, video_id)
            self.task_node.result_info['error_no'] = 1
            self.task_node.result_info['error_msg'] = '请求参数不合法'
        super(GetVideoPlayUrlHandler, self).write_result()

    def get(self):
        self.post()
