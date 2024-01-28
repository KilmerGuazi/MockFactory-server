#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:variableModel.py
@time:2022/03/21
"""

from dataclasses import dataclass
from dataclasses import field
from domain.model import Model


@dataclass
class Variable(Model):
    id: int = field(init=False)
    name: str = None
    type: int = None
    content: str = None
    project_id: int = None
    creator: str = None
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)
