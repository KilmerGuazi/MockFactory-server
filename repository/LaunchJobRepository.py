#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:LaunchJobRepository.py
@time:2022/03/21
"""
from repository.Repository import AbstractRepository
from domain.launchJobModel import LaunchJob, LaunchJobDetail
from sqlalchemy import desc, asc
from flask import current_app
import sys


class LaunchJobRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, launchJob):
        self.session.add(launchJob)
        self.session.commit()
        # 刷新实体
        self.session.refresh(launchJob)
        # 切断实体与session的连接
        self.session.expunge(launchJob)

    def get(self, condition: dict) -> LaunchJob:
        return self.session.query(LaunchJob).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(LaunchJob).filter_by(**condition).order_by(
            desc(LaunchJob.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(LaunchJob).filter_by(**condition).all()

    def update(self, launchJobId, content):
        result = self.session.query(LaunchJob).filter_by(id=launchJobId).update(content)
        self.session.commit()
        return result


class LaunchJobDetailRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, launchJobDetail):
        self.session.add(launchJobDetail)
        self.session.commit()
        # 刷新实体
        self.session.refresh(launchJobDetail)
        # 切断实体与session的连接
        self.session.expunge(launchJobDetail)

    def get(self, condition: dict) -> LaunchJobDetail:
        return self.session.query(LaunchJobDetail).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(LaunchJobDetail).filter_by(**condition).order_by(
            desc(LaunchJobDetail.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(LaunchJobDetail).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(LaunchJobDetail).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def getDetail(self, launchJobId: int) -> LaunchJobDetail:
        return self.session.query(LaunchJobDetail).filter_by(job_id=launchJobId, deleted=0).order_by(
            asc(LaunchJobDetail.order)).all()


if __name__ == '__main__':
    pass
