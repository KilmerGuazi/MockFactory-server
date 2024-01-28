#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:msgtemplate.py
@time:2022/04/02
"""
from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from error import *
from domain.msgTemplateModel import MsgTemplate
from service.MsgTemplateService import MsgTemplateService
import json


class MsgTemplateQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=str, required=True, help='pageSize参数异常:{error_msg}')
        self.param_parse.add_argument('currentPage', type=str, required=True, help='currentPage参数异常:{error_msg}')
        self.param_parse.add_argument('condition', type=str, required=True, help='condition参数异常:{error_msg}')
        self.template_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'type': fields.Integer,
            'template': fields.String,
            'project': fields.Nested({
                'id': fields.Integer,
                'name': fields.String
            }),
            'node': fields.Nested({
                'id': fields.Integer,
                'name': fields.String
            }),
            'tree_path': fields.String,
            'comment': fields.String,
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/msgtemplate/query 查询消息模板
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        mts = MsgTemplateService()
        total, templates = mts.query(request.json['pageSize'], request.json['currentPage'], request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        response = MyResponse.get_success_response(msg='查询成功', data=marshal(templates, self.template_fields),
                                                   append_data=appendData)
        return response


class MsgTemplateSaveApi(Resource):

    def __init__(self):
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('type', type=int, required=True, help='type参数异常:{error_msg}')
        self.param_parse.add_argument('template', type=str, required=True, help='template参数异常:{error_msg}')
        self.param_parse.add_argument('project', type=str, required=True, help='project参数异常:{error_msg}')
        self.param_parse.add_argument('node_id', type=str, required=True, help='node_id参数异常:{error_msg}')
        self.param_parse.add_argument('tree_path', type=str, required=True, help='tree_path参数异常:{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常:{creator}')

    def post(self):
        """
       @api {post} /mock/msgtemplate/save 新建消息模板
       """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        msgTemplate = MsgTemplate()
        msgTemplate.id = request.json['id']
        msgTemplate.name = request.json['name']
        msgTemplate.type = request.json['type']
        msgTemplate.project_id = request.json['project']['id']
        msgTemplate.template = json.dumps(request.json['template'])
        msgTemplate.creator = request.json['creator']
        msgTemplate.comment = request.json['comment']
        msgTemplate.node_id = request.json['node_id']
        msgTemplate.tree_path = request.json['tree_path']
        mts = MsgTemplateService()
        mts.add(msgTemplate)
        return MyResponse.get_success_response(msg='保存消息模板成功!')


if __name__ == '__main__':
    pass
