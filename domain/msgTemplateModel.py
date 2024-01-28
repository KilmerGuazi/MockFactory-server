#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:msgTemplateModel.py
@time:2022/04/02
"""

from dataclasses import dataclass
from dataclasses import field
from domain.model import Model


@dataclass
class MsgTemplate(Model):
    id: int = field(init=False)
    name: str = None
    type: int = None
    template: str = None
    project_id: int = None
    creator: str = None
    deleted: int = 0
    comment: str = None
    node_id: int = 1
    tree_path: str = None
    create_time: str = field(default=None)
    update_time: str = field(default=None)


if __name__ == '__main__':
    pass
