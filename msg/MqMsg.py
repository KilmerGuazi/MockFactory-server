#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:MqMsg.py
@time:2022/04/19
"""
import pika
from flask import current_app


class MqManager:

    def __init__(self, host, vhost, exchange, queue, user, password):
        self.host = host
        self.vhost = vhost
        self.exchange = exchange
        self.queue = queue
        self.user = user
        self.password = password
        self.__connect()

    def __connect(self):
        self.credentials = pika.PlainCredentials(username=self.user, password=self.password)
        self.connectionParam = pika.ConnectionParameters(
            host=self.host,  # broker地址
            virtual_host=self.vhost,  # vhost 地址
            credentials=self.credentials,  # 登陆认证
        )
        self.connection = pika.BlockingConnection(self.connectionParam)
        self.channel = self.connection.channel()

    @property
    def connected(self):
        return self.connection.is_open

    def send(self, message, times=1):
        for i in range(0, times):
            try:
                current_app.logger.info(
                    'mq发送信息:host:{} vhost:{} exchange:{} queue:{} user:{} password:{} channel status: {} message: {}'.format(
                        self.host, self.vhost, self.exchange, self.queue, self.user, self.password,
                        self.channel.is_open, message
                    ))
                self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=message)
                current_app.logger.info('mq消息发送成功!')
            except Exception as e:
                current_app.logger.info('mq消息发送失败：{}'.format(str(e)))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_app.logger.info("mq manager 退出")
        if exc_type is not None and issubclass(exc_type, Exception):
            current_app.logger.info(f"mq异常发生：退出")
        self.connection.close()


if __name__ == '__main__':
    pass
