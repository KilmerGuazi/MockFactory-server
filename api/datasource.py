from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from tool.response import MyResponse
from service.DataSourceService import DataSourceService
from domain.datasourceModel import DataSource
import json


class DataSourceTestApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('ext_info', type=str, required=True, help='ext_info参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/datasource/test 测试数据源链接
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        dss = DataSourceService()
        dss.test(request.json['type'], request.json['ext_info'])
        return MyResponse.get_success_response(msg='数据源测试成功')


class DataSourceSaveApi(Resource):
    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('type', type=int, required=True, help='type参数异常：{error_msg}')
        self.param_parse.add_argument('project', type=int, required=True, help='project参数异常：{error_msg}')
        self.param_parse.add_argument('ext_info', type=dict, required=True, help='ext_info参数异常:{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/datasource/save 数据源保存
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        ds = DataSource()
        ds.id = request.json['id']
        ds.name = request.json['name']
        ds.type = request.json['type']
        ds.project_id = request.json['project']['projectId']
        ds.ext_info = json.dumps(request.json['ext_info'])
        ds.creator = request.json['creator']
        dss = DataSourceService()
        dss.add(ds)
        return MyResponse.get_success_response(msg='保存数据源成功')


class DataSourceQueryApi(Resource):

    def __init__(self):
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=int, required=True, help='pageSize参数异常:{error_msg}')
        self.param_parse.add_argument('currentPage', type=int, required=True, help='currentPage参数异常：{error_msg}')
        self.param_parse.add_argument('condition', type=dict, required=True, help='condition参数异常：{error_msg}')
        self.my_fields = {
            'id': fields.Integer,
            'project': fields.Nested({
                'projectId': fields.Integer(attribute='id'),
                'projectName': fields.String(attribute='name')
            }),
            'name': fields.String,
            'type': fields.Integer,
            'ext_info': fields.String,
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String,
            'deleted': fields.Integer,
            'disabled': fields.Integer,
        }

    def post(self):
        """
        @api {post} /mock/datasource/query 查询数据源
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        ds = DataSourceService()
        total, datasources = ds.query(request.json['pageSize'], request.json['currentPage'],
                                      request.json['condition'])

        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        return MyResponse.get_success_response(msg='查询成功', data=marshal(datasources, self.my_fields),
                                               append_data=appendData)


class DataSourceDeleteApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/datasource/delete 删除数据源
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        ds = DataSourceService()
        ds.delete(request.json['id'])
        response = MyResponse.get_success_response(msg='删除数据源成功')
        return response


class DataSourceDisableApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常:{error_msg}')
        self.param_parse.add_argument('disable', type=int, required=True, help='disable参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/datasource/disable 禁用/启用数据源
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        ds = DataSourceService()
        ds.disable(request.json['id'], request.json['disable'])
        msg = '禁用数据源成功' if request.json['disable'] == 0 else '启用数据源成功'
        return MyResponse.get_success_response(msg=msg)
