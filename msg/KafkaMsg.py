#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:KafkaMsg.py
@time:2022/03/28
"""
from kafka import KafkaProducer
from flask import current_app


class KafkaManager:

    def __init__(self, host, port, topic):
        self.host = host
        self.port = port
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=f'{host}:{port}')

    @property
    def isCurrentProducerConnect(self):
        return self.producer.bootstrap_connected()

    def send(self, msg, times=1, timeout=2):
        for i in range(0, times):
            future = self.producer.send(self.topic, value=self.__encode_msg(msg))
            future.get(timeout=timeout)

    def __encode_msg(self, msg):
        """
        encode消息，str 2 bytes
        """
        return msg.encode("utf8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_app.logger.info("kafka manager 退出")
        if exc_type is not None and issubclass(exc_type, Exception):
            current_app.logger.info(f"kafka异常发生：退出")


if __name__ == '__main__':
    pass
