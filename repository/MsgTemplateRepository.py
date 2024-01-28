#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:MsgTemplateRepository.py
@time:2022/04/02
"""

from repository.Repository import AbstractRepository
from domain.msgTemplateModel import MsgTemplate
from sqlalchemy import desc, and_


class MsgTemplateRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, template):
        self.session.add(template)
        self.session.commit()
        # 刷新实体
        self.session.refresh(template)
        # 切断实体与session的连接
        self.session.expunge(template)

    def get(self, condition: dict) -> MsgTemplate:
        return self.session.query(MsgTemplate).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        rules = self.__getQueryCondition(condition)
        return self.session.query(MsgTemplate).filter(and_(*rules)).order_by(
            desc(MsgTemplate.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        rules = self.__getQueryCondition(condition)
        return self.session.query(MsgTemplate).filter(and_(*rules)).all()

    def listAllFuzzyByTreePath(self, treePath):
        condition = '{}%'.format(treePath)
        return self.session.query(MsgTemplate).filter(MsgTemplate.tree_path.like(condition)).all()

    def update(self, id, content):
        result = self.session.query(MsgTemplate).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def __getQueryCondition(self, condition):
        """
        动态获取查询条件，模糊查询和精确查询
        """
        conditionKeys = condition.keys()
        rules = []
        for key in conditionKeys:
            if key == 'name':
                rules.append(MsgTemplate.name.like('%{}%'.format(condition[key])))
            elif key == 'project_id':
                rules.append(MsgTemplate.project_id == condition[key])
            elif key == 'node_id':
                rules.append(MsgTemplate.node_id == condition[key])
            elif key == 'deleted':
                rules.append(MsgTemplate.deleted == condition[key])
        return rules


if __name__ == '__main__':
    pass
