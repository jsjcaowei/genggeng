# -*- coding: utf-8 -*-
"""
"""
import hashlib

from conf.server_conf import API_PREFIX_CONFIG
from service.const_server import CNST
from util.convert_10_with_62 import base62_encode
from base_model import *

import qrcode
import json
from aliyunsdkvod.request.v20170321 import CreateUploadVideoRequest
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest


class VideoModel(BaseModel):
    """ Video model类
    Methods:
    """

    def __init__(self):
        super(VideoModel, self).__init__()

    @staticmethod
    def create_upload_video(task_node, video_title='', video_file_name='', video_size=0,
                            video_description='', video_cover_url='', upload_IP=''):
        """
        获取视频上传地址和凭证
        :return
            RequestId	    String	请求ID
            VideoId	        String	视频ID
            UploadAddress	String	上传地址
            UploadAuth	    String	上传凭证
        """
        client = task_node.acl_client
        request = CreateUploadVideoRequest.CreateUploadVideoRequest()
        request.set_accept_format('JSON')
        request.set_Title(video_title)  # 视频标题
        request.set_FileName(video_file_name)  # 视频源文件名称
        request.set_FileSize(video_size)  # 视频文件大小
        request.set_Description(video_description)  # 视频描述
        request.set_CoverURL(video_cover_url)  # 自定义视频封面URL地址
        request.set_Privilege(CNST.VIDEO_WATCH_PRIVILGE["public"])  # 视频观看权限
        request.set_IP(upload_IP)  # 上传所在IP地址
        response = json.loads(client.do_action_with_exception(request))
        return response


    @staticmethod
    def get_video_play_auth_info(task_node):
        """获取url对应二维码图片的链接
        :return
            RequestId:	String	请求ID
            VideoMeta:	{
                    VideoId	String	视频ID
                    Title	String	视频标题
                    Duration	Float	视频时长(秒)
                    CoverURL	String	视频封面
                    Status	String	视频状态 }
            PlayAuth:	String	视频播放凭证
        备注：
        Status：
            Uploading	上传中	视频的初始状态，表示正在上传
            UploadFail	上传失败	由于是断点续传，无法确定上传是否失败，故暂不会出现此值
            UploadSucc	上传完成
            Transcoding	转码中
            TranscodeFail	转码失败	转码失败，一般是原片有问题，可在事件通知的转码完成消息得到ErrorMessage失败信息，或提交工单联系我们
            Checking	审核中	在“视频点播控制台-全局设置-审核设置”开启了“先审后发”，转码成功后视频状态会变成审核中，此时视频只能在控制台播放
            Blocked	屏蔽	在审核时屏蔽视频
            Normal	正常	视频可正常播放
        """
        # 参照 https://help.aliyun.com/document_detail/52833.html?spm=5176.doc56124.6.647.C0DoIg
        # {'PlayAuth':'', 'VideoMeta': {Status:'',Duration: float, CoverURL:'', VideoId:'',
        # 'Title':''},'RequestId':}}

        video_id = task_node.business_param['video_id']
        request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)  # 视频ID
        response = json.loads(task_node.acl_client.do_action_with_exception(request))
        gen_log.info('<seq_no=%s> 获取视频点播播放凭证成功, ali_vod_id=%s', task_node.seq_no, video_id)
        return response


    @staticmethod
    def get_play_address_info(task_node):
        """获取视频播放地址
        :return
        RequestId: String
        VideoBase：{
                    VideoId	String	视频ID
                    Title	String	视频标题
                    Duration	String	视频时长(秒)
                    CoverURL	String	视频封面
                    Status	String	视频状态
                    CreationTime	String	视频创建时间，为UTC时间
                    MediaType	String	媒体文件类型，取值：video(视频)，audio(纯音频)
                    }
        PlayInfoList：{ Bitrate	String	视频流码率，单位Kbps
                        Definition	String	视频流清晰度定义, 取值：FD(流畅)，LD(标清)，SD(高清)，HD(超清)，OD(原画)，2K(2K)，4K(4K)
                        Duration	String	视频流长度，单位秒
                        Encrypt	Long	视频流是否加密流，取值：0(否)，1(是)
                        PlayURL	String	视频流的播放地址
                        Format	String	视频流格式，若媒体文件为视频则取值：mp4, m3u8，若是纯音频则取值：mp3
                        Fps	String	视频流帧率，每秒多少帧
                        Size	Long	视频流大小，单位Byte
                        Width	Long	视频流宽度，单位px
                        Height	Long	视频流高度，单位px
                        StreamType	String	视频流类型，若媒体流为视频则取值：video，若是纯音频则取值：audio
                        JobId	String	媒体流转码的作业ID
                        }
        """
        # return : RequestId
        video_id = task_node.business_param['video_id']
        request = GetPlayInfoRequest.GetPlayInfoRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(video_id)
        request.set_AuthTimeout(3600 * 24)  # 播放地址过期时间（只有开启了URL鉴权才生效），默认为3600秒，支持设置最小值为3600秒
        response = json.loads(task_node.acl_client.do_action_with_exception(request))
        return response