from enum import Enum
from tool.response import *
from flask import current_app
import traceback


class BusinessCode(Enum):
    SUCCESS = 10000
    INTERNAL_SERVER_ERROR = 99999
    USER_NOT_EXIST = 90001
    USER_NAME_EMAIL_EXIST = 90011
    ORDER_NOT_EXIST = 90002
    CONNECT_DATASOURCE_FAIL = 90003
    DATASOURCE_NAME_ALREADY_EXIST = 90004
    WORKER_NAME_ALREADY_EXIST = 90005
    VARIABLES_NAME_ALREADY_EXIST = 90006
    PROJECT_NAME_ALREADY_EXIST = 90007
    PRODUCT_LINE_NAME_ALREADY_EXIST = 90008
    MSG_TEMPLATE_NAME_ALREADY_EXIST = 90010
    RUN_SQL_ERROR = 90010
    SEND_KAFKA_TEST_MSG_FAIL = 90011
    SEND_MQ_TEST_MSG_FAIL = 90012
    CANNOT_DELETE_TREE_NODE_HAS_MSG = 90013
    CANNOT_DELETE_WORKER_HAS_PRODUCTLINE = 90014


def register_errors(app):
    # @app.errorhandler(400)
    # def bad_request(e):
    #     return api_abort(return_code.Unauthorized)
    #
    # @app.errorhandler(403)
    # def forbidden(e):
    #     return api_abort(return_code.Forbidden)
    #
    # @app.errorhandler(404)
    # def database_not_found_error_handler(e):
    #     return api_abort(HTTP_STATUS_CODES, message=e.description)

    #
    # @app.errorhandler(405)
    # def method_not_allowed(e):
    #     return api_abort(return_code.Illegalmethod, message='The method is not allowed for the requested URL.')

    # @app.errorhandler(500)
    # def internal_server_error(e):
    #     return api_abort(500, message=e.description)

    # The default_error_handler function as written above will not return any response if the Flask application
    # is running in DEBUG mode.
    @app.errorhandler(Exception)
    def default_error_handler(e):
        current_app.logger.info('exception happen')
        current_app.logger.info(e)
        current_app.logger.error(traceback.print_exc())
        return MyResponse.get_fail_response(error=e)


class MockFactoryDeleteWorkerFailHasProductline(Exception):
    def __init__(self, msg='当前工人存在于产品线中无法删除'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.CANNOT_DELETE_WORKER_HAS_PRODUCTLINE.value

    def __str__(self):
        return self.msg


class MockFactoryDeleteTreeNodeFailHasMsg(Exception):
    def __init__(self, msg='当前节点下包含消息模板，无法删除'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.CANNOT_DELETE_TREE_NODE_HAS_MSG.value

    def __str__(self):
        return self.msg


class MockFactoryMsgTemplateAlreadyExist(Exception):
    def __init__(self, msg='消息模板已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.MSG_TEMPLATE_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockRunSqlException(Exception):
    def __init__(self, msg='执行SQL异常', error=None):
        super().__init__(self)
        self.msg = "{}:{}".format(msg, str(error))
        self.code = BusinessCode.RUN_SQL_ERROR.value

    def __str__(self):
        return self.msg


class MockProductLineNameAlreadyExist(Exception):
    def __init__(self, msg='生产线名称已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.PRODUCT_LINE_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockProjectNameAlreadyExist(Exception):
    def __init__(self, msg='项目名称已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.PROJECT_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryVariablesAlreadyExist(Exception):
    def __init__(self, msg='变量集名称已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.VARIABLES_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryWorkerNameAlreadyExist(Exception):
    def __init__(self, msg='造数工人名称已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.WORKER_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryDataSourceNameAlreadyExist(Exception):
    def __init__(self, msg='数据源名称已存在!'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.DATASOURCE_NAME_ALREADY_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryTestDataSourceFail(Exception):
    def __init__(self, msg='连接数据源失败!'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.CONNECT_DATASOURCE_FAIL.value

    def __str__(self):
        return self.msg


class MockFactoryMqSendTestMsgFail(Exception):
    def __init__(self, msg='发送mq测试数据失败'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.SEND_MQ_TEST_MSG_FAIL.value

    def __str__(self):
        return self.msg


class MockFactoryKafkaSendTestMsgFail(Exception):
    def __init__(self, msg='发送kafka测试数据失败'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.SEND_KAFKA_TEST_MSG_FAIL.value

    def __str__(self):
        return self.msg


class MockFactoryUserNameOrEmailAlreadyExist(Exception):

    def __init__(self, msg='用户名称或邮件地址已存在'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.USER_NAME_EMAIL_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryUserNotExistException(Exception):

    def __init__(self, msg='用户不存在，请先注册！'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.USER_NOT_EXIST.value

    def __str__(self):
        return self.msg


class MockFactoryPasswordInvalidException(Exception):
    def __init__(self, msg='密码不正确，请输入正确的密码！'):
        super().__init__(self)
        self.msg = msg
        self.code = BusinessCode.USER_NOT_EXIST.value

    def __str__(self):
        return self.msg
