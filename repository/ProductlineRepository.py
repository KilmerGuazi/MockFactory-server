#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:ProductlineRepository.py
@time:2022/03/21
"""
from repository.Repository import AbstractRepository
from domain.productlineModel import ProductLine, ProductLineWorkerRelation
from sqlalchemy import desc, and_


class ProductLineRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, productline):
        self.session.add(productline)
        self.session.commit()
        # 刷新实体
        self.session.refresh(productline)
        # 切断实体与session的连接
        self.session.expunge(productline)

    def get(self, condition: dict) -> ProductLine:
        return self.session.query(ProductLine).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(ProductLine).filter_by(**condition).order_by(
            desc(ProductLine.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(ProductLine).filter_by(**condition).all()

    def listAllByIds(self, ids):
        return self.session.query(ProductLine).filter(and_(ProductLine.deleted == 0, ProductLine.id.in_(ids))).all()

    def update(self, id, content):
        result = self.session.query(ProductLine).filter_by(id=id).update(content)
        self.session.commit()
        return result


class ProductLineWorkerRelationRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, productlineRelation):
        self.session.add(productlineRelation)
        self.session.commit()
        # 刷新实体
        self.session.refresh(productlineRelation)
        # 切断实体与session的连接
        self.session.expunge(productlineRelation)

    def get(self, condition: dict) -> ProductLineWorkerRelation:
        return self.session.query(ProductLineWorkerRelation).filter_by(**condition).first()

    def listAll(self, condition: dict):
        return self.session.query(ProductLineWorkerRelation).filter_by(**condition).all()

    def listAllByWorkerIds(self, workerIds=[]):
        return self.session.query(ProductLineWorkerRelation).filter(
            and_(ProductLineWorkerRelation.deleted == 0, ProductLineWorkerRelation.worker_id.in_(workerIds))).all()

    def update(self, id, content):
        result = self.session.query(ProductLineWorkerRelation).filter_by(productline_id=id).update(content)
        self.session.commit()
        return result


if __name__ == '__main__':
    pass
