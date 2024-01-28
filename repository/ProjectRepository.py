#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:ProjectRepository.py
@time:2022/03/15
"""
from repository.Repository import AbstractRepository
from domain.projectModel import Project
from sqlalchemy import desc
from app import App


class ProjectRepository(AbstractRepository):

    def __init__(self):
        super().__init__()
        self.session = App().db.create_scoped_session()

    def add(self, project):
        self.session.add(project)
        self.session.commit()
        # 刷新实体/mock/worker/sql/save
        self.session.refresh(project)
        # 切断实体与session的连接
        self.session.expunge(project)

    def get(self, condition: dict) -> Project:
        return self.session.query(Project).filter_by(**condition).first()

    def listPage(self, start, end, condition: dict) -> list:
        return self.session.query(Project).filter_by(**condition).order_by(
            desc(Project.create_time)).slice(start, end).all()

    def listAll(self, condition: dict):
        return self.session.query(Project).filter_by(**condition).all()

    def update(self, id, content):
        result = self.session.query(Project).filter_by(id=id).update(content)
        self.session.commit()
        return result
