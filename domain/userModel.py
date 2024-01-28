#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:userModel.py
@time:2022/03/17
"""
from dataclasses import dataclass, field
from domain.model import Model


@dataclass
class User(Model):
    id: int = field(init=False)
    name: str = None
    password: str = None
    email: str = None
