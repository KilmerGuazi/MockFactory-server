#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:WorkerRepository.py
@time:2022/03/21
"""
import time
from repository.Repository import AbstractRepository
from domain.workerModel import Worker, WorkerContentSql, WorkerContentMessage
from sqlalchemy import desc


class WorkerRepository(AbstractRepository):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def add(self, worker):
        self.session.add(worker)
        self.session.commit()
        # 刷新实体
        self.session.refresh(worker)
        # 切断实体与session的连接
        self.session.expunge(worker)

    def addWorkerContentMessage(self, workerContentMessage):
        self.session.add(workerContentMessage)
        self.session.commit()
        # 刷新实体
        self.session.refresh(workerContentMessage)
        # 切断实体与session的连接
        self.session.expunge(workerContentMessage)

    def addWorkerContentSql(self, workerContentSql):
        self.session.add(workerContentSql)
        self.session.commit()
        # 刷新实体
        self.session.refresh(workerContentSql)
        # 切断实体与session的连接
        self.session.expunge(workerContentSql)

    def get(self, condition: dict) -> Worker:
        return self.session.query(Worker).filter_by(**condition).first()

    def getWorkerSqlContent(self, condition: dict) -> WorkerContentSql:
        return self.session.query(WorkerContentSql).filter_by(**condition).all()

    def getWorkerMessageContent(self, condition: dict) -> WorkerContentMessage:
        return self.session.query(WorkerContentMessage).filter_by(**condition).all()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(Worker).filter_by(**condition).order_by(
            desc(Worker.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(Worker).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(Worker).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def updateWorkerSqlContent(self, id, content):
        result = self.session.query(WorkerContentSql).filter_by(id=id).update(content)
        self.session.commit()
        return result

    def updateWorkerSqlContentByWorkerId(self, workerId, content):
        result = self.session.query(WorkerContentSql).filter_by(worker_id=workerId).update(content)
        self.session.commit()
        return result

    def updateWorkerMessageContentByWorkerId(self, workerId, content):
        result = self.session.query(WorkerContentMessage).filter_by(worker_id=workerId).update(content)
        self.session.commit()
        return result

    def deleteWorkerMessageContent(self, id):
        result = self.session.query(WorkerContentMessage).filter_by(worker_id=id).update({'deleted': time.time()})
        self.session.commit()
        return result

    def deleteWorkSqlContent(self, id):
        result = self.session.query(WorkerContentSql).filter_by(worker_id=id).update({'deleted': time.time()})
        self.session.commit()
        return result
