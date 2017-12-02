# -*- coding: utf-8 -*-

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import time
import json
import hashlib
from tornado.log import gen_log

from util.oss_client import OSSClient


class BaseService(object):
    """服务基类
    Methods:
    """
    def __init__(self):
        pass
