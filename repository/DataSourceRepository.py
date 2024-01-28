#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:DataSourceRepository.py
@time:2022/03/17
"""
from repository.Repository import AbstractRepository
from domain.datasourceModel import DataSource
from sqlalchemy import desc
from app import App


class DataSourceRepository(AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = App().db.create_scoped_session()

    def add(self, dataSource):
        self.session.add(dataSource)
        self.session.commit()
        # 刷新实体
        self.session.refresh(dataSource)
        # 切断实体与session的连接
        self.session.expunge(dataSource)

    def get(self, condition: dict) -> DataSource:
        return self.session.query(DataSource).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(DataSource).filter_by(**condition).order_by(
            desc(DataSource.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(DataSource).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(DataSource).filter_by(id=id).update(content)
        self.session.commit()
        return result


if __name__ == '__main__':
    pass
