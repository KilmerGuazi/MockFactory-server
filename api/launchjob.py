from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from error import *
from tool.common import *
from service.LaunchJobService import LaunchJobService
from domain.launchJobModel import LaunchJob, LaunchJobDetail


class LaunchJobDetailQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('launchJobId', type=str, required=True, help='launchJobId参数异常:{error_msg}')
        self.launchJobDetail_fields = {
            'launchJobDetailId': fields.Integer(attribute='id'),
            'launchJobDetailName': fields.String(attribute='name'),
            'launchJobDetailOrder': fields.Integer(attribute='order'),
            'launchJobDetailStatus': fields.Integer(attribute='status'),
            'launchJobDetailStartTime': fields.String(attribute='start_time'),
            'launchJobDetailEndTime': fields.String(attribute='end_time'),
            'launchJobDetailLog': fields.String(attribute='log'),
            'worker': fields.Nested({
                'workerId': fields.Integer(attribute='id'),
                'workerName': fields.String(attribute='name')
            })
        }

    def post(self):
        """
        @api {post} /mock/launchJobDetail/query 查询任务
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        launchJobService = LaunchJobService()
        launchJobDetails = launchJobService.queryDetail(request.json['launchJobId'])
        return MyResponse.get_success_response(msg='查询成功', data=marshal(launchJobDetails, self.launchJobDetail_fields))


class LaunchJobQueryApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=str, required=True, help='pageSize参数异常:{error_msg}')
        self.param_parse.add_argument('currentPage', type=str, required=True, help='currentPage参数异常:{error_msg}')
        self.param_parse.add_argument('condition', type=str, required=True, help='condition参数异常：{error_msg}')
        self.launchJob_fields = {
            'launchJobId': fields.Integer(attribute='id'),
            'launchJobName': fields.String(attribute='name'),
            'productLine': fields.Nested({
                'productLineId': fields.Integer(attribute='id'),
                'productLineName': fields.String(attribute='name')
            }),
            'project': fields.Nested({
                'projectId': fields.Integer(attribute='id'),
                'projectName': fields.String(attribute='name')
            }),
            'launchJobStatus': fields.Integer(attribute='status'),
            'launchJobStartTime': fields.String(attribute='start_time'),
            'launchJobEndTime': fields.String(attribute='end_time'),
            'updateTime': fields.String(attribute='update_time'),
            'creator': fields.String
        }

    def post(self):
        """
        @api {post} /mock/launchJob/query 查询任务
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        launchJobService = LaunchJobService()
        total, launchJobs = launchJobService.query(request.json['pageSize'], request.json['currentPage'],
                                                   request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }
        return MyResponse.get_success_response(msg='查询成功', data=marshal(launchJobs, self.launchJob_fields),
                                               append_data=appendData)


class LaunchJobSaveApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('productLine', type=dict, required=True, help='productLine参数异常:{error_msg}')
        self.fields = {
            'launchJobId': fields.Integer(attribute='id'),
            'launchJobName': fields.String(attribute='name'),
            'launchJobStatus': fields.String(attribute='status'),
            'launchJobDetail': fields.List(fields.Nested({
                'detailJobId': fields.Integer(attribute='id'),
                'detailJobName': fields.String(attribute='name'),
                'workerId': fields.String(attribute='worker_id'),
                'workerOrder': fields.Integer(attribute='order'),
                'detailJobStatus': fields.Integer(attribute='status'),
                'detailJobStartTime': fields.String(attribute='start_time'),
                'detailJobEndTime': fields.String(attribute='end_time')
            }))
        }

    def post(self):
        """
        @api {post} /mock/launchJob/save 保存任务
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        launchJob = LaunchJob()
        launchJobService = LaunchJobService()
        launchJob.name = 'Job_{}_{}'.format(request.json['productLine']['productLineName'], time.time())
        launchJob.productline_id = request.json['productLine']['productLineId']
        launchJob.status = 0  # 未开始
        launchJob.creator = request.json['productLine']['creator']
        launchJob.start_time = TimeTool.timestamp2Date(timestamp=time.localtime())
        relations = request.json['productLine']['relations']
        detailList = []
        for relation in relations:
            tmpWorker = relation['worker']
            launchJobDetail = LaunchJobDetail()
            launchJobDetail.name = 'DETAIL_{}_{}'.format(launchJob.name, tmpWorker['workerName'])
            launchJobDetail.job_id = launchJob.id,
            launchJobDetail.worker_id = tmpWorker['workerId'],
            launchJobDetail.order = relation['relationOrder']
            launchJobDetail.creator = request.json['productLine']['creator']
            detailList.append(launchJobDetail)
        launchJob.launchJobDetail = detailList
        launchJobService.add(launchJob)
        return MyResponse.get_success_response(msg='保存生产线成功!', data=marshal(launchJob, self.fields))
