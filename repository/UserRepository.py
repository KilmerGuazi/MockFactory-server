#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:UserRepository.py
@time:2022/03/17
"""
from repository.Repository import AbstractRepository
from domain.userModel import User
from sqlalchemy import desc


class UserRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, user):
        self.session.add(user)
        self.session.commit()
        # 刷新实体
        self.session.refresh(user)
        # 切断实体与session的连接
        self.session.expunge(user)

    def get(self, condition: dict) -> User:
        return self.session.query(User).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(User).filter_by(**condition).order_by(
            desc(User.id)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(User).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(User).filter_by(id=id).update(content)
        self.session.commit()
        return result
