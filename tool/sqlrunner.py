from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pymysql.constants import CLIENT
from error import MockRunSqlException
import re
import json
import jsonpath
from urllib.parse import quote_plus
from app import App
from tool.tranfer import transferMessage


class Runner:

    def __init__(self, info: dict = {}):
        self.info = info
        self.dataSource = self.info.get("dataSource")
        self.db = self.info.get("db")
        self.variables = self.info.get('variables')
        self.sql = self.info.get("content")
        self.context = self.info.get("context")
        self.unionKey = self.info.get("unionKey")
        self.order = self.info.get("order")

    def execute(self):
        self.__transform_sql()
        self.__run_sql()

    def __run_sql(self):
        try:
            extInfo = json.loads(self.dataSource.ext_info)

            # 连接数据库
            connectPath = "mysql+pymysql://{}:{}@{}:{}/{}" \
                .format(extInfo['user'],
                        quote_plus(extInfo['password']),
                        extInfo['host'],
                        extInfo['port'],
                        self.db)
            engine = create_engine(connectPath, connect_args={'client_flag': CLIENT.MULTI_STATEMENTS})
            session = Session(engine, future=True)
            result = session.execute(self.sql)
            session.commit()

            # sql执行完毕后，查看是否需要填充
            tmp_context = self.__fill_context(result)
            # 写入redis并设置过期时间
            if tmp_context is not None:
                if App().redis_client.exists(self.unionKey):
                    tmpValue = json.loads(App().redis_client.get(self.unionKey))
                    tmpValue[self.order] = tmp_context[self.order]
                    App().redis_client.set(self.unionKey, json.dumps(tmpValue))
                else:
                    App().redis_client.set(self.unionKey, json.dumps(tmp_context))
                    # 30分钟后过期
                    App().redis_client.expire(self.unionKey, 60 * 30)
        except Exception as error:
            session.rollback()
            raise MockRunSqlException(error=error)
        finally:
            if session:
                session.close()

    def __fill_context(self, result):
        """
        填充上下文
        """
        if self.context is None or self.context == "":
            # 无需填充
            return None
        # 需要填充
        result_list = [dict(zip(item.keys(), item)) for item in result]
        # 检查查询结果
        if len(result_list) > 1:
            raise MockRunSqlException(error="查询存在多行结果，目前只支持单行结果，请确认")
        if len(result_list) <= 0:
            raise MockRunSqlException(error="查询无结果，无法填充上下文，请确认")
        target_result = result_list[0]
        # 检查上下文json格式
        try:
            current_context = json.loads(self.context)
        except json.JSONDecodeError as error:
            raise MockRunSqlException(error="上下文格式异常，请确认")
        keys = current_context.keys()
        for key in keys:
            # 判断上线文中的key是否在查询结果中存在
            if key not in target_result.keys():
                raise MockRunSqlException(error="当前key {}在查询结果中不存在，请确认".format(key))
            # 判断上下文中key对应的类型
            result_type = type(target_result[key]).__name__
            context_type = current_context[key]
            if context_type in [str.__name__, int.__name__]:
                if context_type != result_type:
                    raise MockRunSqlException(
                        error="当前上下文{}类型{}与查询结果对应列的类型{}不匹配，请确认".format(key, context_type, result_type))
            else:
                raise MockRunSqlException(error='上下文中key:{}的类型{}暂不支持，请确认'.format(key, context_type))
            current_context[key] = target_result[key]
        return {self.order: current_context}

    def __checkInfo(self):
        """
        检查执行信息是否完备
        """
        pass

    def __transform_sql(self):
        """
        转换SQL，主要负责:
        1、将原始SQL中的变量替换
        2、将原始SQL中的上下文变量替换掉
        """
        self.sql = re.sub(r'\$\{([a-zA-z0-9_]+\.?)+\}', self.__transform_sql_handler, self.sql)

    def __transform_sql_handler(self, matched):
        # 通过JsonPath提高定位效率和简化代码
        value = matched.group()
        value = value[2:-1].split('.')
        valueHeader = value[0]
        valueBody = value[1:len(value)]
        path = '$.' + '.'.join(valueBody)
        if valueHeader == '__mf_context_value__':
            # 处理上下文
            content = json.loads(App().redis_client.get(self.unionKey))
            target = jsonpath.jsonpath(content, path)
            return str(target[0])
        else:
            # 处理变量
            for v in self.variables:
                content = json.loads(v.content)
                target = jsonpath.jsonpath(content, path)
                if target:
                    if isinstance(target[0], str):
                        jsonValue = str(target[0])
                    elif isinstance(target[0], int) or isinstance(target[0], float) or isinstance(target[0], complex):
                        jsonValue = str(target[0])
                    elif isinstance(target[0], list) or isinstance(target[0], dict):
                        # 如果是列表、字典类型直接转换成json字符串
                        jsonValue = json.dumps(target[0], ensure_ascii=False)
                    else:
                        pass
                    # 判断是否是mf函数，如果是mf函数则需要特殊处理
                    # 找得到就使用新值，找不到就使用原值
                    jsonValue = transferMessage(jsonValue)
                    return jsonValue
