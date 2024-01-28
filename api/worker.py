from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from error import *
from service.WorkerService import WorkerService


class WorkerDeleteApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/worker/delete 删除工人
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        ws = WorkerService()
        ws.delete(request.json['id'])
        return MyResponse.get_success_response(msg='删除工人成功')


class WorkerQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=int, required=True, help='pageSize参数异常：{error_msg}')
        self.param_parse.add_argument('currentPage', type=int, required=True, help='currentPage参数异常：{error_msg}')
        self.param_parse.add_argument('condition', type=dict, required=True, help='condition参数异常：{error_msg}')
        self.worker_fields = {
            'worker_id': fields.Integer(attribute='id'),
            'type': fields.Integer,
            'worker_name': fields.String(attribute='name'),
            'project': fields.Nested({
                'project_id': fields.Integer(attribute='id'),
                'project_name': fields.String(attribute='name')
            }),
            'creator': fields.String,
            'create_time': fields.String,
            'update_time': fields.String
        }

    def post(self):
        """
        @api {post} /mock/worker/query 查询工人信息
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        ws = WorkerService()
        total, workers = ws.query(request.json['pageSize'], request.json['currentPage'], request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        return MyResponse.get_success_response(msg='查询成功', data=marshal(workers, self.worker_fields),
                                               append_data=appendData)


class WorkerDetailQueryApi(Resource):
    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常：{error_msg}')
        self.param_parse.add_argument('type', type=int, required=True, help='type参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/worker/detail/query 查询工人明细信息
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        ws = WorkerService()
        worker, field = ws.queryDetail(request.json['id'], request.json['type'])
        return MyResponse.get_success_response(msg='查询成功', data=marshal(worker, field))


class SqlWorkerSaveApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        # self.param_parse.add_argument('datasource', type=dict, required=True, help='datasource参与异常:{error_msg}')
        self.param_parse.add_argument('content', type=dict, required=True, help='content参数异常：{error_msg}')
        self.param_parse.add_argument('project', type=dict, required=True, help='project参与异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/worker/sql/save 保存工人
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        ws = WorkerService()
        ws.addSqlWorker(request.json)
        return MyResponse.get_success_response(msg='保存工人成功')


class MessageWorkerSaveApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('name', type=str, required=True, help='name参数异常:{error_msg}')
        self.param_parse.add_argument('datasource', type=dict, required=True, help='datasource参与异常:{error_msg}')
        self.param_parse.add_argument('content', type=list, required=True, help='content参数异常：{error_msg}')
        self.param_parse.add_argument('project', type=dict, required=True, help='project参与异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/worker/message/save 保存消息类型工人
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        ws = WorkerService()
        ws.addMessageWorker(request)
        return MyResponse.get_success_response(msg='保存工人成功')
