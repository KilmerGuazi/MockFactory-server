#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:workerModel.py
@time:2022/03/21
"""
from dataclasses import dataclass
from dataclasses import field


@dataclass
class Worker:
    id: int = None
    type: int = None
    name: str = None
    project_id: int = None
    datasource_id: int = None
    disabled: int = 0
    creator: str = None
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)


@dataclass
class WorkerContentSql:
    id: int = None
    worker_id: int = None
    template_id: int = None
    order: int = None
    deleted: int = 0
    creator: str = None
    create_time: str = field(default=None)
    update_time: str = field(default=None)


@dataclass
class WorkerContentMessage:
    id: int = None
    worker_id: int = None
    template_id: int = None
    order: int = None
    count: int = None
    deleted: int = 0
    creator: str = None
    create_time: str = field(default=None)
    update_time: str = field(default=None)


if __name__ == '__main__':
    pass
