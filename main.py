"""
App启动
"""
from app import App
from flask_restful import Api, request
from flask_redis import FlaskRedis
from error import *
import logging
import datetime as dt
from flask_cors import *
import orm.mapper as orm_mapper
from api.project import ProjectAddApi, ProjectQueryApi, ProjectDeleteApi, ProjectDisableApi
from api.datasource import DataSourceSaveApi, DataSourceQueryApi, DataSourceDisableApi, DataSourceDeleteApi, \
    DataSourceTestApi
from api.variables import VariableQueryApi, VariableBatchQueryApi, VariablesSaveApi, VariablesDeleteApi, \
    VariableQueryBatchApi
from api.worker import WorkerQueryApi, WorkerDeleteApi, SqlWorkerSaveApi, MessageWorkerSaveApi, WorkerDetailQueryApi
from api.productline import ProductLineSaveApi, ProductLineQueryApi, ProductLineDeleteApi, ProductLineLaunchApi, \
    ProductLineDisableApi, ProductLineFavoriteApi
from api.user import UserLoginApi, UserSignInApi, UserListApi
from api.launchjob import LaunchJobSaveApi, LaunchJobQueryApi, LaunchJobDetailQueryApi
from api.msgtemplate import MsgTemplateSaveApi, MsgTemplateQueryApi
from api.msgtree import MessageTreeQueryApi, MessageTreeAddNodeApi, MessageTreeDeleteNodeApi, MessageTreeGetNodePathApi
from api.dataTemplate import DataTemplateSaveApi, DataTemplateQueryApi


class MyLogFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


application = App()
my_app = application.app
# 允许跨域请求
CORS(my_app, supports_credentials=True)
# 注册路由路径
my_app.logger.debug('注册路由路径')
restful_api = Api(my_app)
# api:用户
restful_api.add_resource(UserLoginApi, '/mock/user/login')
restful_api.add_resource(UserSignInApi, '/mock/user/signin')
restful_api.add_resource(UserListApi, '/mock/user/list')

# api:项目
restful_api.add_resource(ProjectAddApi, '/mock/project/add')
restful_api.add_resource(ProjectQueryApi, '/mock/project/query')
restful_api.add_resource(ProjectDeleteApi, '/mock/project/delete')
restful_api.add_resource(ProjectDisableApi, '/mock/project/disable')

# api:数据源
restful_api.add_resource(DataSourceTestApi, '/mock/datasource/test')
restful_api.add_resource(DataSourceSaveApi, '/mock/datasource/save')
restful_api.add_resource(DataSourceQueryApi, '/mock/datasource/query')
restful_api.add_resource(DataSourceDeleteApi, '/mock/datasource/delete')
restful_api.add_resource(DataSourceDisableApi, '/mock/datasource/disable')

# api:变量
restful_api.add_resource(VariableQueryApi, '/mock/variables/query')
restful_api.add_resource(VariableBatchQueryApi, '/mock/variables/queryBatch')
restful_api.add_resource(VariablesSaveApi, '/mock/variables/save')
restful_api.add_resource(VariablesDeleteApi, '/mock/variables/delete')
restful_api.add_resource(VariableQueryBatchApi, '/mock/variables/batchQuery')

# api:数据模板
restful_api.add_resource(DataTemplateSaveApi, '/mock/template/data/save')
restful_api.add_resource(DataTemplateQueryApi, '/mock/template/data/query')

# api:消息模板
restful_api.add_resource(MsgTemplateSaveApi, '/mock/msgtemplate/save')
restful_api.add_resource(MsgTemplateQueryApi, '/mock/msgtemplate/query')

# api:消息树
restful_api.add_resource(MessageTreeQueryApi, '/mock/messagetree/query')
restful_api.add_resource(MessageTreeAddNodeApi, '/mock/messagetree/add')
restful_api.add_resource(MessageTreeDeleteNodeApi, '/mock/messagetree/delete')
restful_api.add_resource(MessageTreeGetNodePathApi, '/mock/messagetree/getNodePath')

# api:工人
restful_api.add_resource(WorkerQueryApi, '/mock/worker/query')
restful_api.add_resource(WorkerDeleteApi, '/mock/worker/delete')
restful_api.add_resource(SqlWorkerSaveApi, '/mock/worker/sql/save')
restful_api.add_resource(MessageWorkerSaveApi, '/mock/worker/message/save')
restful_api.add_resource(WorkerDetailQueryApi, '/mock/worker/detail/query')

# api:生产线
restful_api.add_resource(ProductLineQueryApi, '/mock/productLine/query')
restful_api.add_resource(ProductLineSaveApi, '/mock/productLine/save')
restful_api.add_resource(ProductLineLaunchApi, '/mock/productLine/launch')
restful_api.add_resource(ProductLineDisableApi, '/mock/productLine/disable')
restful_api.add_resource(ProductLineDeleteApi, '/mock/productLine/delete')
restful_api.add_resource(ProductLineFavoriteApi, '/mock/productLine/favorite')

# api:任务
restful_api.add_resource(LaunchJobQueryApi, '/mock/launchJob/query')
restful_api.add_resource(LaunchJobSaveApi, '/mock/launchJob/save')
restful_api.add_resource(LaunchJobDetailQueryApi, '/mock/launchJobDetail/query')


# 定义拦截器
@my_app.before_request
def request_before():
    if request.method == 'POST':
        msg = 'before {method} {path} {cookie} {param}'.format(
            method=request.method,
            path=request.path,
            cookie=request.cookies,
            param=json.loads(request.data)
        )
        my_app.logger.info(msg)


@my_app.after_request
def request_after(response):
    if request.method == 'POST':
        msg = 'after {method} {path} {cookie} {param} {response}'.format(
            method=request.method,
            path=request.path,
            cookie=request.cookies,
            param=request.data,
            response=response.json
        )
        my_app.logger.info(msg)
    return response


# 定义异常处理期
register_errors(my_app)

# 日志
# [time, level, module, function, detail]
logging.basicConfig(level=logging.DEBUG)
log_format = MyLogFormatter(fmt='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                            datefmt='%Y-%m-%d,%H:%M:%S.%f')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)
my_app.logger.addHandler(log_handler)

# 启动mapper
orm_mapper.start()

# 启动
application.run()
