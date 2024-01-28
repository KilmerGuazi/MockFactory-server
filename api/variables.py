from app import App
from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from error import *
from sqlalchemy import and_
from domain.variableModel import Variable
from service.VariableService import VariableService


class VariableBatchQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('ids', type=str, required=True, help='ids参数异常：{error_msg}')
        self.param_parse.add_argument('projectId', type=str, required=True, help='projectId参数异常：{error_msg}')
        self.variable_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'content': fields.String
        }

    def post(self):
        """
        @api {post} /mock/variables/queryBatch 批量查询变量集
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        vs = VariableService()
        variables = vs.batchQuery(request.json['projectId'], request.json['ids'])
        return MyResponse.get_success_response(msg='查询成功', data=marshal(variables, self.variable_fields))


class VariableQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=str, required=True, help='pageSize参数异常:{error_msg}')
        self.param_parse.add_argument('currentPage', type=str, required=True, help='currentPage参数异常:{error_msg}')
        self.param_parse.add_argument('condition', type=str, required=True, help='condition参数异常:{error_msg}')
        self.variable_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'type': fields.Integer,
            'content': fields.String,
            'project': fields.Nested({
                'projectId': fields.Integer(attribute='id'),
                'projectName': fields.String(attribute='name')
            }),
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/variables/query 查询变量
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        vs = VariableService()
        total, variables = vs.query(request.json['pageSize'], request.json['currentPage'], request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        response = MyResponse.get_success_response(msg='查询成功', data=marshal(variables, self.variable_fields),
                                                   append_data=appendData)
        return response


class VariableQueryBatchApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('ids', type=list, nullable=False, required=True, help='ids:{error_msg}')
        self.variable_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'type': fields.Integer,
            'content': fields.String,
            'project': fields.Nested({
                'projectId': fields.Integer(attribute='id'),
                'projectName': fields.String(attribute='name')
            }),
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/variables/batchQuery 批量查询变量
        """
        # 参数校验
        ids = request.json['ids']
        if len(ids) == 0:
            return MyResponse.get_success_response(msg='查询成功', data=marshal([], self.variable_fields))
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        vs = VariableService()
        variables = vs.queryBatch(ids)
        response = MyResponse.get_success_response(msg='查询成功', data=marshal(variables, self.variable_fields))
        return response


class VariablesSaveApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('type', type=int, required=True, help='type参数异常:{error_msg}')
        self.param_parse.add_argument('project', type=str, required=True, help='project参数异常:{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常:{creator}')
        self.my_fields = {
            'id': fields.Integer,
            'name': fields.String,
            'type': fields.Integer,
            'project_id': fields.Integer,
            'creator': fields.String
        }

    def post(self):
        """
        @api {post} /mock/variables/save 新建变量集
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        variable = Variable()
        variable.id = request.json['id']
        variable.name = request.json['name']
        variable.type = request.json['type']
        variable.project_id = request.json['project']['projectId']
        variable.content = request.json['content']
        variable.creator = request.json['creator']
        vs = VariableService()
        vs.add(variable)
        return MyResponse.get_success_response(msg='保存变量集成功!', data=[marshal(variable, self.my_fields)])


class VariablesDeleteApi(Resource):

    def __init__(self):
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=str, required=True, help='id参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/variables/delete 新建变量集
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        vs = VariableService()
        vs.delete(request.json['id'])
        return MyResponse.get_success_response(msg='删除变量集成功')
