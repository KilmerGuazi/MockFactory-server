#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:WorkerService.py
@time:2022/03/21
"""
import time
from app import App
from tool.biz_type import WorkerType
from domain.workerModel import Worker, WorkerContentMessage, WorkerContentSql
from repository.WorkerRepository import WorkerRepository
from repository.ProjectRepository import ProjectRepository
from repository.DataSourceRepository import DataSourceRepository
from repository.MsgTemplateRepository import MsgTemplateRepository
from repository.DataTemplateRepository import DataTemplateRepository
from error import *
from tool.biz_fields import sql_worker_fields, message_worker_fields
from service.ProductlineService import ProductlineService


class WorkerService:

    def __init__(self):
        pass

    def addSqlWorker(self, param):
        cur_session = App().db.create_scoped_session()
        worker = Worker(id=param['id'], name=param['name'],
                        type=param['type'],
                        datasource_id=None, creator=param['creator'],
                        project_id=param['project']['id'])
        content = param['content']
        with WorkerRepository(session=cur_session) as wr, DataSourceRepository() as dsr:
            # datasource = dsr.get({'id': worker.datasource_id, 'deleted': 0})
            # worker.type = datasource.type
            tmpWorker = wr.get({'name': worker.name, 'deleted': 0})
            if worker.id != '':
                # 编辑保存
                if tmpWorker and worker.id != int(tmpWorker.id):
                    raise MockFactoryWorkerNameAlreadyExist(msg='工人名称{}已存在无法保存'.format(worker.name))
                # 更新工人信息
                wr.update(id=worker.id, content={'name': worker.name})
                # 原有内容删除
                wr.deleteWorkSqlContent(id=worker.id)
            else:
                # 新建保存
                if tmpWorker:
                    raise MockFactoryWorkerNameAlreadyExist(msg='工人名称{}已存在无法创建'.format(worker.name))
                worker.id = None
                wr.add(worker)
            for template in content:
                wr.addWorkerContentSql(
                    WorkerContentSql(worker_id=worker.id, template_id=template['template']['id'],
                                     order=template['order']))

    def addMessageWorker(self, param):
        cur_session = App().db.create_scoped_session()
        worker = Worker(id=param.json['id'], name=param.json['name'], datasource_id=param.json['datasource']['id'],
                        creator=param.json['creator'], project_id=param.json['project']['id'])
        content = param.json['content']
        with WorkerRepository(session=cur_session) as wr, DataSourceRepository() as dsr:
            datasource = dsr.get({'id': worker.datasource_id, 'deleted': 0})
            worker.type = datasource.type
            tmpWorker = wr.get({'name': worker.name, 'deleted': 0})
            if worker.id != '':
                # 编辑保存
                if tmpWorker and worker.id != int(tmpWorker.id):
                    raise MockFactoryWorkerNameAlreadyExist(msg='工人名称{}已存在无法保存'.format(worker.name))
                # 更新工人信息
                wr.update(id=worker.id, content={'name': worker.name})
                # 原有内容删除
                wr.deleteWorkerMessageContent(id=worker.id)
            else:
                # 新建保存
                if tmpWorker:
                    raise MockFactoryWorkerNameAlreadyExist(msg='工人名称{}已存在无法创建'.format(worker.name))
                worker.id = None
                wr.add(worker)
            # 更新工人关联内容信息
            for template in content:
                content = WorkerContentMessage(worker_id=worker.id, template_id=template['template']['id'],
                                               order=template['order'], count=template['count'],
                                               creator=worker.creator)
                wr.addWorkerContentMessage(content)

    def delete(self, id: int):
        """
        删除工人
        """
        cur_session = App().db.create_scoped_session()
        with WorkerRepository(session=cur_session) as wr:
            # 生产线是否有使用此工人
            productlineService = ProductlineService()
            productlines = productlineService.queryByWorkerIds([id])
            if len(productlines) > 0:
                raise MockFactoryDeleteWorkerFailHasProductline(
                    msg='当前工人正在被这些生产线使用，无法删除。{}'.format(
                        '\\'.join([productline.name for productline in productlines])))
            else:
                worker = wr.get({'id': id, 'deleted': '0'}, )
                # 删除worker关联内容
                if worker.type == 1:
                    wr.updateWorkerSqlContentByWorkerId(workerId=id, content={'deleted': time.time()})
                else:
                    wr.updateWorkerMessageContentByWorkerId(workerId=id, content={'deleted': time.time()})
                # 删除worker
                result = wr.update(id, {'deleted': time.time()})
            return result

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询数据源
        """
        cur_session = App().db.create_scoped_session()
        with WorkerRepository(session=cur_session) as wr, ProjectRepository() as pr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(wr.listAll(condition))
            workers = wr.listPage(start, end, condition)
            projects = pr.listAll({'deleted': 0})
            for worker in workers:
                tmpProject = list(filter(lambda project: project.id == worker.project_id, projects))[0]
                worker.project = tmpProject
            return total, workers

    def queryDetail(self, id, type):
        """
        查询工人的特定数据
        """
        cur_session = App().db.create_scoped_session()
        with WorkerRepository(cur_session) as wr, ProjectRepository() as pr, DataSourceRepository() as dsr, MsgTemplateRepository(cur_session) as mtr, DataTemplateRepository() as dtr:
            worker = wr.get({'id': id})
            datasource = dsr.get({'id': worker.datasource_id})
            worker.datasource = datasource
            project = pr.get({'id': worker.project_id})
            worker.project = project
            if WorkerType.MYSQL.value == type:
                fields = sql_worker_fields
                content = wr.getWorkerSqlContent({'worker_id': worker.id, 'deleted': 0})
                for tmp in content:
                    tmpTemplate = dtr.get({'id': tmp.template_id})
                    tmp.template = tmpTemplate

            elif WorkerType.KAFKA.value == type or WorkerType.MQ.value == type:
                fields = message_worker_fields
                content = wr.getWorkerMessageContent({'worker_id': worker.id, 'deleted': 0})
                for tmp in content:
                    tmpTemplate = mtr.get({'id': tmp.template_id})
                    tmp.template = tmpTemplate
            worker.content = content
            return worker, fields

    def __transferVariableStr2List(self, variables):
        return variables.split(',')
        # new = []
        # for id in tmp:
        #     new.append(int(id))
        # return new


if __name__ == '__main__':
    pass
