#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:VariableRepository.py
@time:2022/03/21
"""
from repository.Repository import AbstractRepository
from domain.variableModel import Variable
from sqlalchemy import desc, and_
from app import App


class VariableRepository(AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = App().db.create_scoped_session()

    def add(self, variable):
        self.session.add(variable)
        self.session.commit()
        # 刷新实体
        self.session.refresh(variable)
        # 切断实体与session的连接
        self.session.expunge(variable)

    def get(self, condition: dict) -> Variable:
        return self.session.query(Variable).filter_by(**condition).first()

    def getBatch(self, ids: list):
        return self.session.query(Variable).filter(and_(Variable.id.in_(ids), Variable.deleted == 0)).all()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(Variable).filter_by(**condition).order_by(
            desc(Variable.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(Variable).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(Variable).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def batch(self, projectId, variableIds):
        return self.session.query(Variable).filter(
            and_(Variable.deleted == 0, Variable.project_id == projectId, Variable.id.in_(variableIds))).all()


if __name__ == '__main__':
    pass
