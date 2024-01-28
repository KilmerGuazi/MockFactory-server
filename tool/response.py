from flask import Response, make_response
import json


class MyResponse:

    @staticmethod
    def get_success_response(msg: str = '成功', data=[], append_data={}) -> Response:
        response_body = {
            'status': 10000,
            'msg': msg,
            'data': data
        }
        response_body = {**response_body, **append_data}
        response = Response(json.dumps(response_body, ensure_ascii=False))
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        return response

    @staticmethod
    def get_fail_response(msg: str = '失败', error: Exception = None) -> Response:
        response_body = {
            'status': error.code if hasattr(error, 'code') else 99999,
            'msg': '{}:{}'.format(msg, str(error)),
            'data': []
        }
        response = Response(json.dumps(response_body))
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        return response
