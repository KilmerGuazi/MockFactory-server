#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:msgTreeModel.py
@time:2022/05/10
"""

from dataclasses import dataclass
from dataclasses import field
from domain.model import Model


@dataclass
class MsgTree(Model):
    id: int = field(init=False)
    name: str = None
    parent_id: int = None
    creator: str = None
    deleted: int = 0
    create_time: str = field(default=None)
    update_time: str = field(default=None)


if __name__ == '__main__':
    pass
