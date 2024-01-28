#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import random
import re
import time

from tool.common import TimeTool
import time
import json

"""
@author:zhaojiajun
@file:tranfer.py
@time:2022/05/09
"""
# 造数工厂编辑器中的全局通用变量
MF_COMMON_VARIABLE = [
    {
        "name": "mf_current_time_s",
        "value": r'"\$\{(mf_current_time_s)\}"'
    },
    {
        "name": "mf_current_time_ms",
        "value": r'"\$\{(mf_current_time_ms)\}"'
    },
    {
        "name": "mf_current_time",
        "value": r'"\$\{(mf_current_time)\}"'
    },
    {
        "name": "mf.get_time",
        "value": r'"\$\{(mf.get_time)\(([-]?\d+),(\d+),(\d+),(\d+)\)\}"'
    },
    {
        "name": "mf.get_timestamp_s",
        "value": r'"\$\{(mf.get_timestamp_s)\(([-]?\d+),(\d+),(\d+),(\d+)\)\}"'
    },
    {
        "name": "mf.get_timestamp_ms",
        "value": r'"\$\{(mf.get_timestamp_ms)\(([-]?\d+),(\d+),(\d+),(\d+)\)\}"'
    },
    {
        "name": "mf.random_choose",
        "value": r'\$\{(mf.random_choose)\(\[(([\u4e00-\u9fa5_a-zA-Z0-9]+,?)+)\]\)\}'
    },
    {
        "name": "mf.date2timestamp",
        "value": r'\$\{(mf.date2timestamp)\((\d+-\d+-\d+ \d+:\d+:\d+)\)\}'
    },
    {
        "name": "mf.dateOffset",
        "value": r'\$\{(mf.dateOffset)\(([-]?\d+),(\d+),(\d+),(\d+)\)\}'
    }
]


def transferMessage(content):
    """
    转化消息中的变量信息
    """
    for variable in MF_COMMON_VARIABLE:
        content = re.sub(variable['value'], transferHandler, content)
    return content


def transferHandler(matched):
    value = matched.group(1)
    if 'mf_current_time_s' == value:
        return str(TimeTool.timestamp())
    elif 'mf_current_time_ms' == value:
        return str(TimeTool.timestampMS())
    elif 'mf_current_time' == value:
        return "\"{}\"".format(TimeTool.timestamp2Date(timestamp=time.localtime(time.time())))
    elif 'mf.get_time' == value:
        dayOffset = int(matched.group(2))
        h = int(matched.group(3))
        m = int(matched.group(4))
        s = int(matched.group(5))
        return "\"{}\"".format(str(TimeTool.getTimeOfDayOffset(dayOffset, h, m, s)))
    elif 'mf.get_timestamp_s' == value:
        dayOffset = int(matched.group(2))
        h = int(matched.group(3))
        m = int(matched.group(4))
        s = int(matched.group(5))
        return str(round(TimeTool.getTimeOfDayOffset(dayOffset, h, m, s).timestamp()))
    elif 'mf.get_timestamp_ms' == value:
        dayOffset = int(matched.group(2))
        h = int(matched.group(3))
        m = int(matched.group(4))
        s = int(matched.group(5))
        return str(round(TimeTool.getTimeOfDayOffset(dayOffset, h, m, s).timestamp() * 1000))
    elif 'mf.random_choose' == value:
        items = matched.group(2)
        items = items.replace("'", "").split(',')
        return random.choice(items)
    elif 'mf.date2timestamp' == value:
        items = matched.group(2)
        return str(TimeTool.date2Timestamp(items))
    elif 'mf.dateOffset' == value:
        dayOffset = int(matched.group(2))
        h = int(matched.group(3))
        m = int(matched.group(4))
        s = int(matched.group(5))
        return str(TimeTool.getDateOfDayOffset(dayOffset, h, m, s))

    else:
        return "unknown variable"
