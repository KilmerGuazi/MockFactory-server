#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:Repository.py
@time:2022/03/15
"""
import abc
from flask import current_app
from domain.model import Model


class AbstractRepository(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_app.logger.info("repository 退出")
        current_app.logger.info(f"x:{exc_type}")
        if exc_type is not None and issubclass(exc_type, Exception):
            current_app.logger.info(f"异常发生：{self.session} 回滚")
            self.session.rollback()
        self.session.close()
        current_app.logger.info(f"{self.session} 关闭")


if __name__ == '__main__':
    pass
