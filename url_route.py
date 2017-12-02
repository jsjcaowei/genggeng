# -*- coding: utf-8 -*-


from handler import *
from handler import video_handler

url_route = [
    # 获取微信公众账号的access token
    (r'/video/get_video_list', wx_handler.GetWXAccessToken),
    (r'/video/get_upload_auth', video_handler.GetVideoUploadHandler),
    (r'/video/save_video_info', video_handler.SaveVideoHandler),

    (r'/video/get_video_play_auth', video_handler.GetVideoPlayAuthHandler),
    (r'/video/get_video_play_url', video_handler.GetVideoPlayUrlHandler),
    (r'/video/get_video_list', video_handler.GetVideoListHandler)



]
