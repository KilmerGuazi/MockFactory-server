#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:biz_fields.py
@time:2022/04/07
"""
from flask_restful import fields

# sql类型工人field
sql_worker_fields = {
    'id': fields.Integer,
    'type': fields.Integer,
    'name': fields.String,
    'project': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'content': fields.List(fields.Nested({
        'id': fields.Integer,
        'order': fields.Integer,
        'template': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        })
    })),
    'creator': fields.String,
    'create_time': fields.String,
    'update_time': fields.String,
    'deleted': fields.Integer,
    'disabled': fields.Integer
}

# kafka,mq类型工人field
message_worker_fields = {
    'id': fields.Integer,
    'type': fields.Integer,
    'name': fields.String,
    'datasource': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'project': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'content': fields.List(fields.Nested({
        'id': fields.Integer,
        'order': fields.Integer,
        'count': fields.Integer,
        'template': fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
            'template': fields.String
        })
    })),
    'creator': fields.String,
    'create_time': fields.String,
    'update_time': fields.String,
    'deleted': fields.Integer,
    'disabled': fields.Integer
}

if __name__ == '__main__':
    pass
