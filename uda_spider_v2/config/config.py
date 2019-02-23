# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os

# 拉取数据间隔时间
TIME_SLEEP = 2

# 每个职位拉取的最大页数
MAX_PAGE =5

LOGGER_FORMAT = "%(asctime)s-%(name)s-%(levelname)s-%(message)s"
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
