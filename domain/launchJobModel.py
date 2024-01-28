#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:launchJobModel.py
@time:2022/03/21
"""
from dataclasses import dataclass
from dataclasses import field


@dataclass
class LaunchJob:
    id: int = field(init=False)
    name: str = None
    productline_id: int = None
    status: int = field(default=0)
    start_time: str = field(default=None)
    end_time: str = field(default=None)
    creator: str = field(default="unknown")
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)


@dataclass
class LaunchJobDetail:
    id: int = field(init=False)
    name: str = None
    job_id: int = None
    worker_id: int = None
    order: int = None
    status: int = field(default=0)
    start_time: str = field(default=None)
    end_time: str = field(default=None)
    creator: str = field(default="unknown")
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)
    log: str = field(default=None)


if __name__ == '__main__':
    pass
