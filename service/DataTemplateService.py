#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
data template 数据模板业务

@author:zhaojiajun
@file:DataTemplateService.py
@time:2022/10/13
"""
from app import App
from tool.common import TimeTool
from domain.dataTemplateModel import DataTemplate, DataTemplateDetail
from domain.variableModel import Variable
from repository.DataTemplateRepository import DataTemplateRepository, DataTemplateDetailRepository
from repository.ProjectRepository import ProjectRepository
from repository.DataSourceRepository import DataSourceRepository
from repository.VariableRepository import VariableRepository


class DataTemplateService:

    def __init__(self):
        pass

    def save(self, param):
        """
        保存数据模板
        """
        dataTemplate = DataTemplate(
            name=param['name'],
            project_id=param['project']['id'],
            creator=param['creator']
        )
        # cur_session = App().db.create_scoped_session()
        id = param['id']
        with DataTemplateRepository() as dtr, DataTemplateDetailRepository() as dtdr:
            if not id:
                # 新建
                # 保存data template
                dtr.add(dataTemplate)
                # 保存data template detail
                detail = param['detail']
                for tmpDetail in detail:
                    dataTemplateDetail = DataTemplateDetail(
                        data_template_id=dataTemplate.id,
                        comment=tmpDetail['comment'],
                        order=tmpDetail['order'],
                        datasource_id=tmpDetail['datasource']['id'],
                        db=tmpDetail['db'],
                        variables_id=str(tmpDetail['variable']),
                        content=tmpDetail['content'],
                        context=tmpDetail['context'],
                        creator=dataTemplate.creator
                    )
                    dtdr.add(dataTemplateDetail)
            else:
                # 编辑
                update_content = {
                    "name": param['name'],
                    "project_id": param['project']['id'],
                    "create_time": param['create_time']
                }
                dtr.update(id, update_content)
                detail = param['detail']
                dtdr.deleteByDataTemplateId(id)
                for tmpDetail in detail:
                    dataTemplateDetail = DataTemplateDetail(
                        data_template_id=id,
                        comment=tmpDetail['comment'],
                        order=tmpDetail['order'],
                        datasource_id=tmpDetail['datasource']['id'],
                        db=tmpDetail['db'],
                        variables_id=str(tmpDetail['variable']),
                        content=tmpDetail['content'],
                        context=tmpDetail['context'],
                        creator=dataTemplate.creator
                    )
                    dtdr.add(dataTemplateDetail)

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询数据模板
        """
        with DataTemplateRepository() as dtr, \
                DataTemplateDetailRepository() as dtdr, \
                ProjectRepository() as pr, \
                DataSourceRepository() as dr, \
                VariableRepository() as vr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(dtr.listAll(condition))
            dataTemplates = dtr.listPage(start, end, condition)
            # 查询数据模板明细
            dataTemplateDetails = dtdr.listAll({'deleted': 0})
            # 查询项目
            projects = pr.listAll({})
            # 查询数据源
            datasources = dr.listAll({})
            # 查询变量
            variables = vr.listAll({})
            # 拼接数据
            for dataTemplate in dataTemplates:
                tmpProject = list(filter(lambda p: p.id == dataTemplate.project_id, projects))[0]
                dataTemplate.project = tmpProject
                tmpDetails = list(filter(lambda d: d.data_template_id == dataTemplate.id, dataTemplateDetails))
                for detail in tmpDetails:
                    tmpDataSource = list(filter(lambda d: d.id == detail.datasource_id, datasources))[0]
                    detail.datasource = tmpDataSource
                    if detail.variables_id == '[]':
                        detail.variable = []
                        continue
                    variablesIds = detail.variables_id.strip('[').strip(']').split(',')
                    # targetVariables.extend(list(filter(lambda v: v.id == int(variableId), variables)))
                    detail.variable = variablesIds
                dataTemplate.detail = tmpDetails
        return total, dataTemplates
