#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:ProductlineService.py
@time:2022/03/21
"""
import time
from domain.productlineModel import ProductLine, ProductLineWorkerRelation
from repository.ProductlineRepository import ProductLineRepository, ProductLineWorkerRelationRepository
from repository.WorkerRepository import WorkerRepository
from repository.ProjectRepository import ProjectRepository
from repository.LaunchJobRepository import LaunchJobRepository, LaunchJobDetailRepository
from repository.DataSourceRepository import DataSourceRepository
from repository.VariableRepository import VariableRepository
from repository.DataTemplateRepository import DataTemplateRepository, DataTemplateDetailRepository
from domain.productlineModel import ProductLine, ProductLineWorkerRelation
from service.MsgTemplateService import MsgTemplateService
from domain.launchJobModel import LaunchJob, LaunchJobDetail
from error import *
from app import App
from tool.common import TimeTool
from tool.sqlrunner import Runner
from tool.tranfer import transferMessage
from flask import current_app
from msg.KafkaMsg import KafkaManager
from msg.MqMsg import MqManager
import json
import traceback


class ProductlineService:

    def __init__(self):
        pass

    def add(self, productline, relations):
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(cur_session) as plr, ProductLineWorkerRelationRepository(
                cur_session) as plwrr:
            tmpProductline = plr.get({'name': productline.name, 'deleted': 0})
            if productline.id != '':
                # 编辑保存
                # 更新生产线
                plr.update(productline.id, {'name': productline.name})
                plwrr.update(productline.id, {'deleted': time.time()})
                for relation in relations:
                    productlineWorkerRelation = ProductLineWorkerRelation()
                    productlineWorkerRelation.order = relation.get('relationOrder')
                    productlineWorkerRelation.worker_id = relation.get('worker').get('workerId')
                    productlineWorkerRelation.productline_id = productline.id
                    productlineWorkerRelation.creator = productline.creator
                    plwrr.add(productlineWorkerRelation)
            else:
                # 新建保存
                if tmpProductline:
                    raise MockProductLineNameAlreadyExist(msg='生产线名称{}已存在无法保存'.format(productline.name))
                productline.id = None
                plr.add(productline)
                for relation in relations:
                    productlineWorkerRelation = ProductLineWorkerRelation()
                    productlineWorkerRelation.order = relation.get('relationOrder')
                    productlineWorkerRelation.worker_id = relation.get('worker').get('workerId')
                    productlineWorkerRelation.productline_id = productline.id
                    productlineWorkerRelation.creator = productline.creator
                    plwrr.add(productlineWorkerRelation)

    def query(self, pageSize, currentPage, condition):
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(cur_session) as plr, ProductLineWorkerRelationRepository(
                cur_session) as plwrr, ProjectRepository() as pr, WorkerRepository(cur_session) as wr:
            projects = pr.listAll({'deleted': 0})
            workers = wr.listAll({'deleted': 0})
            relations = plwrr.listAll({'deleted': 0})
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(plr.listAll(condition))
            productlines = plr.listPage(start, end, condition)
            for productline in productlines:
                tmpProject = list(filter(lambda p: p.id == productline.project_id, projects))[0]
                tmpRelations = list(filter(lambda r: r.productline_id == productline.id, relations))
                for relation in tmpRelations:
                    relation.worker = list(filter(lambda worker: relation.worker_id == worker.id, workers))[0]
                productline.project = tmpProject
                productline.relations = tmpRelations
            return total, productlines

    def queryByWorkerIds(self, ids=[]):
        """
        根据workerId查找生产线
        """
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(cur_session) as plr, ProductLineWorkerRelationRepository(
                cur_session) as plwrr:
            productLineRelations = plwrr.listAllByWorkerIds(ids)
            return plr.listAllByIds(ids=[relation.productline_id for relation in productLineRelations])

    def delete(self, id):
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(session=cur_session) as plr, ProductLineWorkerRelationRepository(
                session=cur_session) as plwr:
            plwr.update(id, {'deleted': time.time()})
            return plr.update(id, {'deleted': time.time()})

    def disable(self, id, disable):
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(session=cur_session) as plr:
            disableStatus = 1 if disable == 0 else 0
            return plr.update(id, {'disabled': disableStatus})

    def favorite(self, id, favorite):
        cur_session = App().db.create_scoped_session()
        with ProductLineRepository(session=cur_session) as plr:
            return plr.update(id, {'favorite': favorite})

    def launch(self, productline, job):
        launchJobId = job.get('launchJobId')
        launchJobDetailList = job.get('launchJobDetail')
        # 按照工人顺序排序
        launchJobDetailList = sorted(launchJobDetailList, key=lambda tmp: tmp['workerOrder'])
        cur_session = App().db.create_scoped_session()
        with LaunchJobRepository(cur_session) as ljr, LaunchJobDetailRepository(cur_session) as ljdr, WorkerRepository(
                cur_session) as wr, DataSourceRepository() as dsr, VariableRepository() as vr:
            # 更新生产线任务状态"未开始"到"进行中"
            ljr.update(launchJobId, dict(status=1))
            # 一个生产线中可以有多个工人，每个工人对应一个任务明细
            for detail in launchJobDetailList:
                detailId = detail.get('detailJobId')
                detailWorkerId = detail.get('workerId')
                worker = wr.get({'id': detailWorkerId, 'deleted': 0})
                if worker.type in [1]:
                    # sql工人
                    # 每个工人可以执行多个内容（模板）
                    workerContent = wr.getWorkerSqlContent({'worker_id': worker.id, 'deleted': 0})
                    # 按照order 排序
                    # 工作执行他的多个工作内容
                    # 更新任务明细状态->运行中
                    ljdr.update(detailId,
                                dict(status=1, start_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                    try:
                        self.__SqlWorkerExecute(workerContent, launchJobId, detailId)
                    except Exception as error:
                        log = traceback.format_exc()
                        # 更新子任务状态-> 异常
                        ljdr.update(detailId,
                                    dict(log=log, status=-1,
                                         end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        # 更新任务状态-> 异常
                        ljr.update(job["launchJobId"],
                                   dict(status=-1, end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        return
                elif worker.type in [4]:
                    # kafka消息工人
                    datasource = dsr.get({'id': worker.datasource_id, 'deleted': 0})
                    workerContent = wr.getWorkerMessageContent({'worker_id': worker.id, 'deleted': 0})
                    try:
                        self.__doKafkaWorkContent(workerContent, datasource)
                    except Exception as error:
                        log = traceback.format_exc()
                        # 更新子任务状态-> 异常
                        ljdr.update(detailId,
                                    dict(log=log, status=-1,
                                         end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        # 更新任务状态-> 异常
                        ljr.update(job["launchJobId"],
                                   dict(status=-1, end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        return
                elif worker.type in [5]:
                    # mq消息工人
                    datasource = dsr.get({'id': worker.datasource_id, 'deleted': 0})
                    workerContent = wr.getWorkerMessageContent({'worker_id': worker.id, 'deleted': 0})
                    try:
                        self.__doMqWorkerContent(workerContent, datasource)
                    except Exception as error:
                        log = traceback.format_exc()
                        # 更新子任务状态-> 异常
                        ljdr.update(detailId,
                                    dict(log=log, status=-1,
                                         end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        # 更新任务状态-> 异常
                        ljr.update(job["launchJobId"],
                                   dict(status=-1, end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
                        return
            # 更新任务明细状态->已完成
            ljdr.update(detailId,
                        dict(status=2, end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))
            # 更新生产线任务状态->已完成
            ljr.update(launchJobId,
                       dict(status=2, end_time=TimeTool.timestamp2Date(timestamp=time.localtime())))

    def __SqlWorkerExecute(self, workerContent, launchJobId, detailJobId):
        """
        sql工作开始工作
        """
        # 一个工人可以有多个工作内容（SQL模板），在工作执行先按照order进行排序
        workerContentSortedList = sorted(workerContent, key=lambda tmp: tmp.order)
        with DataTemplateDetailRepository() as dtdr, DataSourceRepository() as dsr, VariableRepository() as vr:
            # 依次执行任务
            # preUnionKey = ""
            for content in workerContentSortedList:
                templateId = content.template_id
                # 当前工作明细
                workerDetailList = dtdr.getAllDetailByTemplateId(data_template_id=templateId)
                # 执行每一个工作明细
                workerDetailSortedList = sorted(workerDetailList, key=lambda tmp: tmp.order)

                # 工人下的每个工作内容都有一个UnionKey,工作中的上下文范围存在于一个UnionKey中，不能跨content
                workerContentUnionKey = "{}_{}_{}_{}_{}".format(launchJobId, detailJobId, content.worker_id, content.id,
                                                                templateId)
                for detail in workerDetailSortedList:
                    dataSource = dsr.get({"id": detail.datasource_id})
                    variable = [] if detail.variables_id == '[]' else vr.getBatch(
                        ids=detail.variables_id.strip('[').strip(']').split(','))
                    # 执行工作
                    runner = Runner(info={
                        "dataSource": dataSource,
                        "variables": variable,
                        "db": detail.db,
                        "content": detail.content,
                        "context": detail.context,
                        # 当前执行的唯一key：任务id_子任务id_工人id_数据模板id_数据模板明细id
                        "unionKey": workerContentUnionKey,
                        "order": detail.order
                    })
                    runner.execute()

    def __doKafkaWorkContent(self, workerContent, datasource):
        """
        执行kafka工人的消息推送任务
        """
        mts = MsgTemplateService()
        extInfo = json.loads(datasource.ext_info)
        kafkaManager = KafkaManager(host=extInfo['host'], port=extInfo['port'], topic=extInfo['topic'])
        for content in workerContent:
            current_app.logger.info('current worker content:', content)
            template = mts.queryTemplate(content.template_id).template
            template = transferMessage(template)
            current_app.logger.info('send message:', template)
            kafkaManager.send(msg=template, times=content.count)
            time.sleep(1)

    def __doMqWorkerContent(self, workerContent, datasource):
        """
        执行kafka工人的消息推送任务
        """
        mts = MsgTemplateService()
        extInfo = json.loads(datasource.ext_info)
        mqManager = MqManager(extInfo['host'], extInfo['virtual_host'], extInfo['exchange'], extInfo['queue'],
                              extInfo['user'], extInfo['password'])
        for content in workerContent:
            current_app.logger.info('current worker content:', content)
            template = mts.queryTemplate(content.template_id).template
            template = transferMessage(template)
            current_app.logger.info('send message:', template)
            mqManager.send(message=template, times=content.count)
            time.sleep(1)


if __name__ == '__main__':
    pass
