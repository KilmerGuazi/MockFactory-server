from error import *
from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from service.ProductlineService import ProductlineService
from domain.productlineModel import ProductLine, ProductLineWorkerRelation


class ProductLineLaunchApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('productLine', type=dict, required=True, help='productLine参数异常:{error_msg}')
        self.param_parse.add_argument('launchJob', type=dict, required=True, help='launchJob参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/productLine/launch 启动生产线
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        pls = ProductlineService()
        pls.launch(request.json['productLine'], request.json['launchJob'])
        return MyResponse.get_success_response(msg='运行成功')


class ProductLineQueryApi(Resource):

    def __init__(self):
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('pageSize', type=str, required=True, help='pageSize参数异常：{error_msg}')
        self.param_parse.add_argument('currentPage', type=str, required=True, help='currentPage参数异常：{error_msg}')
        self.param_parse.add_argument('condition', type=str, required=True, help='condition参数异常：{error_msg}')
        self.productLine_fields = {
            'productLineId': fields.Integer(attribute='id'),
            'productLineName': fields.String(attribute='name'),
            'updateTime': fields.String(attribute='update_time'),
            'creator': fields.String,
            'disabled': fields.Integer,
            'favorite': fields.Integer,
            'project': fields.Nested({
                'projectId': fields.Integer(attribute='id'),
                'projectName': fields.String(attribute='name')
            }),
            'relations': fields.List(fields.Nested({
                'relationId': fields.Integer(attribute='id'),
                'relationOrder': fields.Integer(attribute='order'),
                'worker': fields.Nested({
                    'workerId': fields.Integer(attribute='id'),
                    'workerName': fields.String(attribute='name'),
                })
            }))
        }

    def post(self):
        """
        @api {post} /mock/productLine/query 查询生产线
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        pls = ProductlineService()
        total, productlines = pls.query(request.json['pageSize'], request.json['currentPage'],
                                        request.json['condition'])
        appendData = {
            'total': total,
            'pageSize': request.json['pageSize'],
            'currentPage': request.json['currentPage']
        }

        return MyResponse.get_success_response(msg='查询成功', data=marshal(productlines, self.productLine_fields),
                                               append_data=appendData)


class ProductLineSaveApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('productLineId', type=str, required=True, help='productLineId参数异常：{error_msg}')
        self.param_parse.add_argument('productLineName', type=str, required=True,
                                      help='productLineName参数异常：{error_msg}')
        self.param_parse.add_argument('projectId', type=str, required=True, help='projectId参数异常：{error_msg}')
        self.param_parse.add_argument('relations', type=str, required=True, help='relations参数异常：{error_msg}')
        self.param_parse.add_argument('creator', type=str, required=True, help='creator参数异常:{error_msg}')

    def post(self):
        """
        @api {post} /mock/productLine/save 保存生产线
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        pls = ProductlineService()
        pl = ProductLine()
        pl.id = request.json['productLineId']
        pl.name = request.json['productLineName']
        pl.project_id = request.json['projectId']
        pl.creator = request.json['creator']
        pls.add(pl, request.json['relations'])
        return MyResponse.get_success_response(msg='保存生产线成功!', data=[])


class ProductLineFavoriteApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常：{error_msg}')
        self.param_parse.add_argument('favorite', type=int, required=True, help='favorite参数异常：{error_msg}')

    def post(self):
        """
        @api{post} /mock/productLine/favorite 收藏
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        pls = ProductlineService()
        pls.favorite(request.json['id'], request.json['favorite'])
        return MyResponse.get_success_response(msg='收藏成功')


class ProductLineDeleteApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常：{error_msg}')

    def post(self):
        """
        @api{post} /mock/productLine/delete 删除数据源
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务处理
        pls = ProductlineService()
        pls.delete(request.json['id'])
        return MyResponse.get_success_response(msg='删除数据成功')


class ProductLineDisableApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('id', type=int, required=True, help='id参数异常:{error_msg}')
        self.param_parse.add_argument('disabled', type=int, required=True, help='disabled参数异常：{error_msg}')

    def post(self):
        """
        @api {post} /mock/productLine/disable
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        pls = ProductlineService()
        pls.disable(request.json['id'], request.json['disabled'])
        msg = '禁用生产线成功' if request.json['disabled'] == 0 else '启用生产线成功'
        return MyResponse.get_success_response(msg=msg)
