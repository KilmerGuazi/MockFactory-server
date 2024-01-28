#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
data_template 数据模型

@author:zhaojiajun
@file:dataTemplateModel.py
@time:2022/10/13
"""
from dataclasses import dataclass
from dataclasses import field


@dataclass
class DataTemplate:
    id: int = field(init=False)
    name: str = None
    project_id: int = None
    create_time: str = None
    update_time: str = None
    creator: str = None
    deleted: int = 0


@dataclass
class DataTemplateDetail:
    id: int = field(init=False)
    data_template_id: int = None
    comment: str = None
    order: int = None
    datasource_id: int = None
    db: str = None
    variables_id: int = None
    content: str = None
    context: str = None
    create_time: str = None
    update_time: str = None
    creator: str = None
    deleted: int = 0


if __name__ == '__main__':
    pass
