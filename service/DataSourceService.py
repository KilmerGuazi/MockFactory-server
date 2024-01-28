#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:DataSourceService.py
@time:2022/03/17
"""
import time
from repository.DataSourceRepository import DataSourceRepository
from repository.ProjectRepository import ProjectRepository
from app import App
from flask import current_app
from error import MockFactoryDataSourceNameAlreadyExist, MockFactoryTestDataSourceFail, MockFactoryKafkaSendTestMsgFail, \
    MockFactoryMqSendTestMsgFail
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from kafka import KafkaProducer
from kafka.errors import kafka_errors
from msg.KafkaMsg import KafkaManager
from msg.MqMsg import MqManager


class DataSourceService:

    def __init__(self):
        pass

    def __testMySql(self, host, port, user, password):
        url = f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}"
        engine = create_engine(url)
        connection = engine.connect()
        if connection.closed:
            raise MockFactoryTestDataSourceFail()
        if 'connection' in locals().keys():
            current_app.logger.info('关闭测试连接')
            connection.close()
        return True

    def __testKafka(self, host, port, topic):
        km = KafkaManager(host, port, topic)
        if not km.isCurrentProducerConnect:
            raise MockFactoryTestDataSourceFail('连接kafka失败')
        km.send('test_send_kafka_msg')

    def __testMq(self, host, vhost, exchange, queue, user, password):
        mqm = MqManager(host, vhost, exchange, queue, user, password)
        if not mqm.connected:
            raise MockFactoryTestDataSourceFail('连接mq失败')
        mqm.send('test_send_mq_msg')

    def test(self, datasourceType, extInfo):
        if datasourceType == 1:
            # mysql
            self.__testMySql(extInfo['host'], extInfo['port'], extInfo['user'], extInfo['password'])
        elif datasourceType == 4:
            # kafka
            self.__testKafka(extInfo['host'], extInfo['port'], extInfo['topic'])
        elif datasourceType == 5:
            # mq
            self.__testMq(extInfo['host'], extInfo['virtual_host'], extInfo['exchange'], extInfo['queue'],
                          extInfo['user'], extInfo['password'])

    def add(self, datasource):
        with DataSourceRepository() as dsr:
            tmpDataSource = dsr.get({'name': datasource.name, 'deleted': 0})
            if datasource.id != '':
                # 编辑保存
                if tmpDataSource and datasource.id != int(tmpDataSource.id):
                    raise MockFactoryDataSourceNameAlreadyExist(msg='数据源名称{}已存在无法保存'.format(datasource.name))
                dsr.update(datasource.id, {
                    'name': datasource.name,
                    'ext_info': datasource.ext_info,
                    'creator': datasource.creator
                })
            else:
                # 新建保存
                if tmpDataSource:
                    raise MockFactoryDataSourceNameAlreadyExist(msg='数据源名称{}已存在无法创建'.format(datasource.name))
                datasource.id = None
                dsr.add(datasource)

    def query(self, pageSize: int, currentPage: int, condition: dict):
        """
        查询数据源
        """
        with DataSourceRepository() as dsr, ProjectRepository() as pr:
            condition = dict(filter(lambda item: item[1] != '', condition.items()))
            start = (currentPage - 1) * pageSize
            end = start + pageSize
            condition['deleted'] = 0
            total = len(dsr.listAll(condition))
            dataSources = dsr.listPage(start, end, condition)
            projects = pr.listAll(dict(deleted=0))
            for dataSource in dataSources:
                tmpProject = list(filter(lambda p: p.id == dataSource.project_id, projects))[0]
                dataSource.project = tmpProject
            return total, dataSources

    def delete(self, id: int):
        """
        删除数据源
        """
        with DataSourceRepository() as dsr:
            result = dsr.update(id, {'deleted': time.time()})
            return result

    def disable(self, id: int, disabled: int):
        """
        禁用/启用数据源
        """
        with DataSourceRepository() as dsr:
            disableStatus = 1 if disabled == 0 else 0
            result = dsr.update(id, {'disabled': disableStatus})
            return result
