#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:productlineModel.py
@time:2022/03/21
"""
from dataclasses import dataclass
from dataclasses import field


@dataclass
class ProductLine:
    id: int = field(init=False)
    name: str = None
    project_id: int = None
    disabled: int = 0
    creator: str = None
    deleted: int = 0
    favorite: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)


@dataclass
class ProductLineWorkerRelation:
    id: int = field(init=False)
    productline_id: int = None
    worker_id: int = None
    order: int = None
    creator: str = None
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)


if __name__ == '__main__':
    pass
