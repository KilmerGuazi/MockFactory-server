#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:UserService.py
@time:2022/03/17
"""
from app import App
from domain.userModel import User
from repository.UserRepository import UserRepository
from error import *


class UserService:

    def __init__(self):
        pass

    def signIn(self, user: User):
        """
        注册
        """
        cur_session = App().db.create_scoped_session()
        with UserRepository(session=cur_session) as ur:
            tmpUser = ur.get({'name': user.name})
            tmpUser1 = ur.get({'email': user.email})
            if tmpUser or tmpUser1:
                raise MockFactoryUserNameOrEmailAlreadyExist()
            else:
                ur.add(user)

    def loginIn(self, user: User):
        """
        登陆
        """
        cur_session = App().db.create_scoped_session()
        with UserRepository(session=cur_session) as ur:
            tmpUser = ur.get({'email': user.email})
            if not tmpUser:
                raise MockFactoryUserNotExistException()
            if tmpUser.password != user.password:
                raise MockFactoryPasswordInvalidException()
            return tmpUser

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询项目
        """
        cur_session = App().db.create_scoped_session()
        with UserRepository(session=cur_session) as ur:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(ur.listAll(condition))
            projects = ur.listPage(start, end, condition)
            return total, projects

    def queryAll(self):
        """
        查询所有用户
        """
        cur_session = App().db.create_scoped_session()
        with UserRepository(session=cur_session) as ur:
            allUser = ur.listAll({})
            total = len(allUser)
            return total, allUser

    def delete(self, id: int):
        """
        删除项目
        """
        with ProjectRepository() as pr:
            result = pr.update(id, {'deleted': time.time()})
            return result

    def disable(self, id: int, disabled: int):
        """
        禁用项目
        """
        with ProjectRepository() as pr:
            disableStatus = 1 if disabled == 0 else 0
            result = pr.update(id, {'disabled': disableStatus})
            return result
