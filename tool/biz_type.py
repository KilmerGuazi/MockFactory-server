#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:biz_type.py
@time:2022/04/07
"""
from enum import Enum, unique


@unique
class WorkerType(Enum):
    MYSQL = 1
    CLICKHOUSE = 2
    REDIS = 3
    KAFKA = 4
    MQ = 5
    INTERFACE = 6


if __name__ == '__main__':
    pass
