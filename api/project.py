#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:ProjectRepository.py
@time:2022/03/16
"""

from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from domain.projectModel import Project
from service.ProjectService import ProjectService
from error import *


class ProjectAddApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=str, required=True, help='id参数异常：{error_msg}')
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常：{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常：{error_msg}')
        self.my_fields = {
            'id': fields.String,
            'name': fields.String,
            'creator': fields.String
        }

    def post(self):
        """
        @api {post} /mock/project/add 新建项目
        """
        self.param_parse.parse_args(http_error_code=400)
        project = Project(id=request.json['id'], name=request.json['name'], creator=request.json['creator'])
        ps = ProjectService()
        ps.add(project)
        return MyResponse.get_success_response(msg='保存项目成功!', data=[marshal(project, self.my_fields)])


class ProjectQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=str, required=True, help='pageSize参数异常：{error_msg}')
        self.param_parse.add_argument('currentPage', type=str, required=True, help='currentPage参数异常：{error_msg}')
        self.my_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'creator': fields.String,
            'disabled': fields.Integer,
            'deleted': fields.Integer,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/project/query 查询项目
        """
        ps = ProjectService()
        total, projects = ps.query(request.json['pageSize'], request.json['currentPage'],
                                   request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        response = MyResponse.get_success_response(msg='查询成功', data=marshal(projects, self.my_fields),
                                                   append_data=appendData)
        return response


class ProjectDeleteApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/project/delete 删除项目
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        ps = ProjectService()
        ps.delete(request.json['id'])
        return MyResponse.get_success_response(msg='删除项目成功')


class ProjectDisableApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常：{error_msg}')
        self.param_parse.add_argument('disabled', type=int, required=True, help='disabled参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/project/disable 禁用/启用项目
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        ps = ProjectService()
        ps.disable(request.json['id'], request.json['disabled'])
        msg = '禁用项目成功' if request.json['disabled'] == 0 else '启用项目成功'
        return MyResponse.get_success_response(msg=msg)
