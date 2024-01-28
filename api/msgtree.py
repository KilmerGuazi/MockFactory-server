#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:msgtree.py
@time:2022/05/10
"""

from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from service.MessageTreeService import MessageTreeService
from tool.response import MyResponse
import json


class MessageTreeQueryApi(Resource):

    def __init__(self):
        self.fields = {
            'id': fields.Integer,
            'label': fields.String,
            'parent_id': fields.Integer,
            'children': fields.List(fields.Nested({

            }))
        }

    def get(self):
        """
        @api {post} /mock/messagetree/query 查询消息树
        """
        mts = MessageTreeService()
        tree = mts.query()
        response = MyResponse.get_success_response(msg='查询成功', data=[tree])
        return response


class MessageTreeAddNodeApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('parent_id', type=int, required=True, help='parent_id参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/messagetree/add 增加树节点
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        mts = MessageTreeService()
        mts.add(request.json['name'], request.json['parent_id'])
        response = MyResponse.get_success_response(msg='添加节点成功', data=[])
        return response


class MessageTreeDeleteNodeApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常:{error_msg}')

    def post(self):
        """
       @api {post} /mock/messagetree/delete 删除树节点
       """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        mts = MessageTreeService()
        mts.delete(request.json['id'])
        response = MyResponse.get_success_response(msg='删除节点成功', data=[])
        return response


class MessageTreeGetNodePathApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('node_id', type=int, required=True, help='node_id参数异常:{error_msg}')

    def post(self):
        """
       @api {post} /mock/messagetree/getNodePath 获取节点路径
       """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        mts = MessageTreeService()
        path = mts.getNodePath(request.json['node_id'])
        response = MyResponse.get_success_response(msg='添加节点成功',
                                                   data={'node_id': request.json['node_id'], 'node_path': path})
        return response


if __name__ == '__main__':
    pass
