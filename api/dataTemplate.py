#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
data template 数据模板API

@author:zhaojiajun
@file:dataTemplate.py
@time:2022/10/13
"""
from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from service.DataTemplateService import DataTemplateService
from tool.response import MyResponse


class DataTemplateSaveApi(Resource):

    def __init__(self):
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('project', type=str, required=True, help='project参数异常:{error_msg}')
        self.param_parse.add_argument('detail', type=object, required=True, help='detail参数异常:{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常:{creator}')

    def post(self):
        """
        @api {post} /mock/template/data/save 保存数据模板
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        dataTemplateService = DataTemplateService()
        dataTemplateService.save(param=request.json)
        return MyResponse.get_success_response(msg='保存数据模板成功')


class DataTemplateQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=int, required=True, help='pageSize参数异常：{error_msg}')
        self.param_parse.add_argument('currentPage', type=int, required=True, help='currentPage参数异常：{error_msg}')
        self.param_parse.add_argument('condition', type=dict, required=True, help='condition参数异常：{error_msg}')
        # 响应体
        self.dataTemplateFields = {
            'id': fields.Integer,
            'name': fields.String,
            'project': fields.Nested({
                'id': fields.Integer,
                'name': fields.String
            }),
            'detail': fields.List(
                fields.Nested({
                    'id': fields.Integer,
                    'data_template_id': fields.Integer,
                    'comment': fields.String,
                    'order': fields.Integer,
                    'datasource': fields.Nested({
                        'id': fields.Integer,
                        'name': fields.String
                    }),
                    'db': fields.String,
                    'variable': fields.List(
                        fields.Integer(default=None),
                    ),
                    'content': fields.String,
                    'context': fields.String,
                    'deleted': fields.Integer
                })
            ),
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/template/data/query 查询数据模板
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        dataTemplateService = DataTemplateService()
        total, workers = dataTemplateService.query(request.json['pageSize'], request.json['currentPage'],
                                                   request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        return MyResponse.get_success_response(msg='查询成功', data=marshal(workers, self.dataTemplateFields),
                                               append_data=appendData)
