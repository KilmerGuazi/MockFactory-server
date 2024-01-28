#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
data template 数据模板操作

@author:zhaojiajun
@file:DataTemplateRepository.py
@time:2022/10/13
"""
from sqlalchemy import desc
from domain.dataTemplateModel import DataTemplate, DataTemplateDetail
from repository.Repository import AbstractRepository
from tool.common import TimeTool
from app import App


class DataTemplateRepository(AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = App().db.create_scoped_session()

    def add(self, dataTemplate):
        self.session.add(dataTemplate)
        self.session.commit()
        # 刷新实体
        self.session.refresh(dataTemplate)
        # 切断实体与session的连接
        self.session.expunge(dataTemplate)

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(DataTemplate).filter_by(**condition).order_by(
            desc(DataTemplate.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(DataTemplate).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(DataTemplate).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def get(self, condition: dict):
        return self.session.query(DataTemplate).filter_by(**condition).first()


class DataTemplateDetailRepository(AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = App().db.create_scoped_session()

    def add(self, dataTemplateDetail):
        self.session.add(dataTemplateDetail)
        self.session.commit()
        # 刷新实体
        self.session.refresh(dataTemplateDetail)
        # 切断实体与session的连接
        self.session.expunge(dataTemplateDetail)

    def listAll(self, condition: dict):
        return self.session.query(DataTemplateDetail).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(DataTemplateDetail).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def deleteByDataTemplateId(self, id):
        result = self.session.query(DataTemplateDetail).filter_by(data_template_id=id, deleted=0).update(
            {"deleted": TimeTool.timestamp()})
        self.session.commit()
        return result

    def get(self, id):
        self.session.query(DataTemplateDetail).filter_by(id=id, deleted=0)

    def getAllDetailByTemplateId(self, data_template_id):
        result = self.session.query(DataTemplateDetail).filter_by(data_template_id=data_template_id, deleted=0)
        return result


if __name__ == '__main__':
    pass
