from flask import request
from flask_restful import Resource, marshal, fields, reqparse
from service.UserService import UserService
from domain.userModel import User
from tool.response import MyResponse


class UserLoginApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser(bundle_errors=True)
        self.param_parse.add_argument('email', type=str, required=True, help='email参数异常:{error_msg}')
        self.param_parse.add_argument('password', type=str, required=True, help='password参数异常:{error_msg}')
        self.my_fields = {
            'id': fields.String,
            'email': fields.String,
            'name': fields.String
        }

    def post(self):
        """
        @api {post} /mock/user/login 登陆用户
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)

        # 业务
        us = UserService()
        user = User()
        user.email = request.json['email']
        user.password = request.json['password']
        user = us.loginIn(user)
        return MyResponse.get_success_response(msg='登陆成功!', data=[marshal(user, self.my_fields)])


class UserSignInApi(Resource):

    def __init__(self):
        # 参数校验
        self.param_parse = reqparse.RequestParser()
        self.param_parse.add_argument('email', type=str, required=True, help='请求参数中必须包含email邮件数据')
        self.param_parse.add_argument('name', type=str, required=True, help='请求参数中必须包含name名称数据')
        self.param_parse.add_argument('password', type=str, required=True, help='请求参数中必须包含password密码数据')
        self.my_fields = {
            'id': fields.String,
            'email': fields.String,
            'name': fields.String
        }

    def post(self):
        """
        @api {post} /mock/user/signin 注册用户
        """
        # 参数校验
        self.param_parse.parse_args(http_error_code=400)
        # 业务
        us = UserService()
        user = User()
        user.email = request.json['email']
        user.name = request.json['name']
        user.password = request.json['password']
        us.signIn(user)
        return MyResponse.get_success_response(msg='注册用户成功!', data=[marshal(user, self.my_fields)])


class UserListApi(Resource):

    def __init__(self):
        self.response_fields = {
            'id': fields.Integer,
            'email': fields.String,
            'name': fields.String
        }

    def get(self):
        """
        @api {get} /mock/user/list 查询所有用户
        """
        us = UserService()
        total, users = us.queryAll()
        return MyResponse.get_success_response(msg='查询所有用户成功', data=marshal(users, self.response_fields))
