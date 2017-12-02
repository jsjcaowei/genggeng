# -*- coding: utf-8 -*-

import hashlib
import json
from tornado.log import gen_log
from util.http_client import HttpClient


class BaseModel(object):
    """Model基类
    Methods:
    """
    def __init__(self):
        pass
