#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:MsgTemplateService.py
@time:2022/04/02
"""
from error import MockFactoryMsgTemplateAlreadyExist
from repository.MsgTemplateRepository import MsgTemplateRepository
from repository.MessageTreeRepository import MessageTreeRepository
from repository.ProjectRepository import ProjectRepository
from app import App


class MsgTemplateService:

    def __init__(self):
        pass

    def add(self, template):
        cur_session = App().db.create_scoped_session()
        with MsgTemplateRepository(session=cur_session) as mtr:
            tmpTemplate = mtr.get({'name': template.name, 'deleted': 0})
            if template.id != '':
                # 编辑保存
                if tmpTemplate and template.id != int(tmpTemplate.id):
                    raise MockFactoryMsgTemplateAlreadyExist(msg='消息模板名称{}已存在无法保存'.format(template.name))
                mtr.update(template.id, {
                    'name': template.name,
                    'template': template.template,
                    'comment': template.comment
                })
            else:
                # 新建保存
                if tmpTemplate:
                    raise MockFactoryMsgTemplateAlreadyExist(msg='消息模板名称{}已存在无法保存'.format(template.name))
                template.id = None
                mtr.add(template)

    def query(self, pageSize: int, currentPage: int, condition: dict):
        cur_session = App().db.create_scoped_session()
        with MsgTemplateRepository(session=cur_session) as mtr, MessageTreeRepository(session=cur_session) as msgtr, \
                ProjectRepository() as pr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(mtr.listAll(condition))
            templates = mtr.listPage(start, end, condition)
            projects = pr.listAll({'deleted': 0})
            nodes = msgtr.listAll({'deleted': 0})
            for template in templates:
                tmpProjects = list(filter(lambda project: project.id == template.project_id, projects))
                template.project = tmpProjects[0]
                tmpTreeNodes = list(filter(lambda node: node.id == template.node_id, nodes))
                if len(tmpTreeNodes) > 0:
                    template.node = tmpTreeNodes[0]

            return total, templates

    def queryTemplate(self, id: int):
        cur_session = App().db.create_scoped_session()
        with MsgTemplateRepository(session=cur_session) as mtr:
            template = mtr.get({'id': id, 'deleted': 0})
            return template


if __name__ == '__main__':
    pass
