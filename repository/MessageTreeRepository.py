#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:MessageTreeRepository.py
@time:2022/05/12
"""
from repository.Repository import AbstractRepository
from domain.msgTreeModel import MsgTree
from sqlalchemy import desc, and_


class MessageTreeRepository(AbstractRepository):

    def add(self, node):
        self.session.add(node)
        self.session.commit()
        # 刷新实体
        self.session.refresh(node)
        # 切断实体与session的连接
        self.session.expunge(node)

    def get(self):
        pass

    def __init__(self, session):
        super().__init__()
        self.session = session

    def listAll(self, condition: dict):
        return self.session.query(MsgTree).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(MsgTree).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def listAllByIds(self, ids):
        return self.session.query(MsgTree).filter(MsgTree.id.in_(ids)).all


if __name__ == '__main__':
    pass
