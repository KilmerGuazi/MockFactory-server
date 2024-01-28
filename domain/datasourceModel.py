#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:datasourceModel.py
@time:2022/03/17
"""

from dataclasses import dataclass
from dataclasses import field
from domain.model import Model


@dataclass
class DataSource(Model):
    id: int = field(init=False)
    name: str = None
    type: int = None
    project_id: int = None
    ext_info: str = field(default=None)
    creator: str = field(default="unknown")
    disabled: int = 0
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)
