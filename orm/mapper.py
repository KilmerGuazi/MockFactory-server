#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:mapper.py
@time:2022/03/15
"""

"""sqlalchemy"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Table, UniqueConstraint
from sqlalchemy import FetchedValue
from sqlalchemy.orm import registry

"""domain"""
from domain.projectModel import Project
from domain.datasourceModel import DataSource
from domain.userModel import User
from domain.variableModel import Variable
from domain.workerModel import Worker, WorkerContentMessage, WorkerContentSql
from domain.productlineModel import ProductLine, ProductLineWorkerRelation
from domain.launchJobModel import LaunchJob, LaunchJobDetail
from domain.msgTemplateModel import MsgTemplate
from domain.msgTreeModel import MsgTree
from domain.dataTemplateModel import DataTemplate, DataTemplateDetail

mapper_registry = registry()

# 用户
user = Table(
    'user',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(255), nullable=False, unique=True, info='邮箱'),
    Column('password', String(255), nullable=False, info='密码'),
    Column('name', String(255), nullable=False, unique=True, info='用户名'),
    UniqueConstraint('email', 'name', name='uk_email_name')
)

# 项目
project = Table(
    'project',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, info='主键id'),
    Column('name', String(100), nullable=False, info='项目名称'),
    Column('creator', String(100), nullable=False, info='创建人'),
    Column('disabled', Integer, server_default=FetchedValue(), info='禁用状态,0:未禁用,1:已禁用'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,null:未删除,!null:删除'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间')
)

# 数据源
datasource = Table(
    'data_source',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, unique=True, info='数据源名称'),
    Column('type', Integer, nullable=False, server_default=FetchedValue(),
           info='数据集类型,1: MYSQL, 2:CLICKHOUSE,3:REDIS,4:KAFKA,5:MQ,6:INTERFACE'),
    Column('project_id', Integer, nullable=False, info='项目id'),
    Column('ext_info', String(510), nullable=False, server_default=FetchedValue(), info='数据源连接拓展信息'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', Integer, server_default=FetchedValue(), info='删除状态,0:未删除,1:已删除'),
    Column('disabled', server_default=FetchedValue(), info='禁用状态,0:未禁用,1:已禁用')
)

# 变量集
variables = Table(
    'variables',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, info='主键id'),
    Column('name', String(100), nullable=False, info='变量名称只能是英文且小写'),
    Column('type', Integer, nullable=False, server_default=FetchedValue(), info='变量集类型,1: JSON, 2:XML'),
    Column('content', String(255), nullable=False, info='变量json数据'),
    Column('project_id', Integer, nullable=False, info='项目id'),
    Column('creator', String(100), nullable=False, info='创建人'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,null:未删除,!null:删除'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    UniqueConstraint('name', 'deleted', name='uk_name_deleted')
)

# 数据模板
dataTemplate = Table(
    'data_template',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, nullable=False, info='主键id'),
    Column('name', String(255), nullable=False, info='模板名称'),
    Column('project_id', nullable=False, info='项目id'),
    Column('create_time', nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', nullable=False, info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    UniqueConstraint('name', 'deleted', name='uk_name_deleted')
)
# 数据模板明细
dataTemplateDetail = Table(
    'data_template_detail',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, info='主键id'),
    Column('data_template_id', Integer, nullable=False, info='模板id'),
    Column('comment', String(255), nullable=False, info='备注'),
    Column('order', Integer, nullable=False, info='顺序'),
    Column('datasource_id', Integer, nullable=False, info='数据源id'),
    Column('db', String(255), nullable=False, info='数据库名称'),
    Column('variables_id', Integer, nullable=True, info='变量id'),
    Column('content', String, nullable=False, info='内容'),
    Column('context', String, nullable=True, info='上下文'),
    Column('create_time', nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', nullable=False, info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    UniqueConstraint('data_template_id', 'deleted', name='uk_data_template_id_deleted')
)

# 消息模板
msgTemplate = Table(
    'msg_template',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, info='主键id'),
    Column('name', String(100), nullable=False, info='消息模板名称'),
    Column('type', Integer, nullable=False, server_default=FetchedValue(), info='变量集类型,1: JSON'),
    Column('template', nullable=False, info='模板'),
    Column('project_id', nullable=False, info='项目id'),
    Column('creator', nullable=False, info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,null:未删除,!null:删除'),
    Column('comment', String(255), server_default=FetchedValue(), info='备注'),
    Column('node_id', Integer, nullable=False, server_default=FetchedValue(), info='树节点id'),
    Column('tree_path', String(255), nullable=False, server_default=FetchedValue(), info='树节点路径'),
    Column('create_time', nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    UniqueConstraint('name', 'deleted', name='uk_name_deleted')
)

# 消息树
msgTree = Table(
    'msg_tree',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, info='主键id'),
    Column('name', String(255), nullable=False, info='节点名称'),
    Column('parent_id', Integer, nullable=False, info='父节点id'),
    Column('creator', server_default=FetchedValue(), info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    Column('create_time', nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    UniqueConstraint('name', 'parent_id', 'deleted', name='uk_parentid_name_deleted')
)

# 工人
worker = Table(
    'worker',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('type', Integer, nullable=False, info='工人类型,1：sql,2:rule,3:接口,4:混合'),
    Column('name', String(255), nullable=False, info='工人名称'),
    Column('project_id', Integer, nullable=False, info='项目id'),
    Column('datasource_id', Integer, nullable=False, info='数据源id'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', server_default=FetchedValue(), info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    Column('disabled', Integer, server_default=FetchedValue(), info='禁用状态,0:未禁用,1:已禁用'),
    UniqueConstraint('name', 'deleted', name='uk_name_deleted')
)

workerContentSql = Table(
    'worker_content_sql',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('worker_id', Integer, nullable=False, info='工人id'),
    Column('template_id', Integer, nullable=False, info='数据模板id'),
    Column('order', Integer, nullable=False, info='消息顺序'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除')
)

workerContentMessage = Table(
    'worker_content_message',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('worker_id', Integer, nullable=False, info='工人id'),
    Column('template_id', Integer, nullable=False, info='消息模板id'),
    Column('order', Integer, nullable=False, info='消息顺序'),
    Column('count', Integer, nullable=False, info='发送次数'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除')
)

# 生产线
productline = Table(
    'productline',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, info='生产线名称'),
    Column('project_id', nullable=False, info='项目id'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    Column('disabled', server_default=FetchedValue(), info='禁用状态,0:未禁用,1:已禁用'),
    Column('favorite', Integer, nullable=False, server_default=FetchedValue(), info='收藏：0 : 否,1:是'),
    UniqueConstraint('name', 'deleted', name='uk_name_deleted')
)

# 生产线和工人的关系
productlineWorkerRelation = Table(
    'productline_worker_relations',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('productline_id', Integer, nullable=False, info='项目id'),
    Column('worker_id', Integer, nullable=False, info='工人id'),
    Column('order', Integer, nullable=False, info='工作顺序'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', server_default=FetchedValue(), info='创建人'),
    Column('deleted', nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除')
)

# 任务
launchJob = Table(
    'launch_job',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, info='任务名称'),
    Column('productline_id', Integer, nullable=False, info='生产线id'),
    Column('status', Integer, nullable=False, server_default=FetchedValue(), info='任务状态,0:未开始,1:进行中,2:成功,-1:异常'),
    Column('start_time', DateTime, info='任务开始时间'),
    Column('end_time', DateTime, info='任务结束时间'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', DateTime, nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除')
)

# 任务明细
launchJobDetail = Table(
    'launch_job_detail',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False, info='任务明细名称'),
    Column('job_id', Integer, nullable=False, info='任务id'),
    Column('worker_id', Integer, nullable=False, info='工人id'),
    Column('order', Integer, nullable=False, info='顺序'),
    Column('status', Integer, nullable=False, server_default=FetchedValue(), info='任务状态,0:未开始,1:进行中,2:完成,-1:异常'),
    Column('start_time', DateTime, info='任务开始时间'),
    Column('end_time', DateTime, info='任务结束时间'),
    Column('create_time', DateTime, nullable=False, server_default=FetchedValue(), info='创建时间'),
    Column('update_time', nullable=False, server_default=FetchedValue(), info='更新时间'),
    Column('creator', String(11), server_default=FetchedValue(), info='创建人'),
    Column('deleted', Integer, nullable=False, server_default=FetchedValue(), info='是否删除,0:未删除,>0:删除'),
    Column('log', String, server_default=FetchedValue(), info='日志')
)


def start():
    mapper_registry.map_imperatively(Project, project)
    mapper_registry.map_imperatively(DataSource, datasource)
    mapper_registry.map_imperatively(User, user)
    mapper_registry.map_imperatively(Variable, variables)
    mapper_registry.map_imperatively(DataTemplate, dataTemplate)
    mapper_registry.map_imperatively(DataTemplateDetail, dataTemplateDetail)
    mapper_registry.map_imperatively(MsgTemplate, msgTemplate)
    mapper_registry.map_imperatively(MsgTree, msgTree)
    mapper_registry.map_imperatively(Worker, worker)
    mapper_registry.map_imperatively(WorkerContentMessage, workerContentMessage)
    mapper_registry.map_imperatively(WorkerContentSql, workerContentSql)
    mapper_registry.map_imperatively(ProductLine, productline)
    mapper_registry.map_imperatively(ProductLineWorkerRelation, productlineWorkerRelation)
    mapper_registry.map_imperatively(LaunchJob, launchJob)
    mapper_registry.map_imperatively(LaunchJobDetail, launchJobDetail)
