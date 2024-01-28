#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:ProjectService.py
@time:2022/03/15
"""
import time

from app import App
from domain.projectModel import Project
from repository.ProjectRepository import ProjectRepository
from error import MockProjectNameAlreadyExist


class ProjectService:

    def __init__(self):
        pass

    def add(self, project: Project):
        """
        新增项目
        """
        with ProjectRepository() as pr:
            # 判断项目是否存在
            tmpProject = pr.get({'name': project.name, 'deleted': 0})
            if project.id != '':
                if tmpProject and tmpProject.id != int(project.id):
                    raise MockProjectNameAlreadyExist()
                pr.update(project.id, dict(name=project.name))
            else:
                if tmpProject:
                    raise MockProjectNameAlreadyExist()
                project.id = None
                pr.add(project)

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询项目
        """
        with ProjectRepository() as pr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(pr.listAll(condition))
            projects = pr.listPage(start, end, condition)
            return total, projects

    def delete(self, id: int):
        """
        删除项目
        """
        with ProjectRepository() as pr:
            result = pr.update(id, {'deleted': time.time()})
            return result

    def disable(self, id: int, disabled: int):
        """
        禁用项目
        """
        with ProjectRepository() as pr:
            disableStatus = 1 if disabled == 0 else 0
            result = pr.update(id, {'disabled': disableStatus})
            return result
