#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:VariableService.py
@time:2022/03/21
"""
from app import App
from repository.VariableRepository import VariableRepository
from repository.ProjectRepository import ProjectRepository
from error import *
import time


class VariableService:

    def __init__(self):
        pass

    def add(self, variable):
        with VariableRepository() as vr:
            tmpVariable = vr.get({'name': variable.name, 'deleted': 0})
            if variable.id != '':
                # 编辑保存
                if tmpVariable and variable.id != int(tmpVariable.id):
                    raise MockFactoryVariablesAlreadyExist(msg='变量名称{}已存在无法保存'.format(variable.name))
                vr.update(variable.id, {
                    'content': variable.content
                })
            else:
                # 新建保存
                if tmpVariable:
                    raise MockFactoryVariablesAlreadyExist(msg='变量名称{}已存在无法创建'.format(variable.name))
                variable.id = None
                vr.add(variable)

    def delete(self, id: int):
        """
        删除变量
        """
        with VariableRepository() as vr:
            result = vr.update(id, {'deleted': time.time()})
            return result

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询数据源
        """
        with VariableRepository() as vr, ProjectRepository() as pr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(vr.listAll(condition))
            variables = vr.listPage(start, end, condition)
            projects = pr.listAll({'deleted': 0})
            for variable in variables:
                tmpProjects = list(filter(lambda project: project.id == variable.project_id, projects))
                variable.project = tmpProjects[0]
            return total, variables

    def queryBatch(self, ids: list):
        """
        批量查询变量
        """
        with VariableRepository() as vr, ProjectRepository() as pr:
            variables = vr.getBatch(ids)
            projects = pr.listAll({'deleted': 0})
            for variable in variables:
                tmpProjects = list(filter(lambda project: project.id == variable.project_id, projects))
                variable.project = tmpProjects[0]
            return variables

    def batchQuery(self, projectId, variableIds):
        with VariableRepository() as vr:
            return vr.batch(projectId, variableIds)


if __name__ == '__main__':
    pass
