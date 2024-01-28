#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:zhaojiajun
@file:MessageTreeService.py
@time:2022/05/12
"""
from app import App
from repository.MessageTreeRepository import MessageTreeRepository
from repository.MsgTemplateRepository import MsgTemplateRepository
from domain.msgTreeModel import MsgTree
from error import MockFactoryDeleteTreeNodeFailHasMsg
import time


class MessageTreeService:

    def __init__(self):
        pass

    def query(self):
        """
        查询整棵消息树
        """
        cur_session = App().db.create_scoped_session()
        with MessageTreeRepository(session=cur_session) as mtr:
            allNode = mtr.listAll({'deleted': 0})
            allNode.sort(key=lambda node: node.parent_id)
            return self.__getTree(allNode)

    def add(self, childNodeName, parentNodeId):
        """
        给树的某个父节点添加子节点
        """
        cur_session = App().db.create_scoped_session()
        with MessageTreeRepository(session=cur_session) as mtr:
            node = MsgTree()
            node.name = childNodeName
            node.parent_id = parentNodeId
            mtr.add(node)

    def delete(self, nodeId):
        """
        删除树的某个节点
        节点下存在消息模板则不允许删除
        """
        cur_session = App().db.create_scoped_session()
        with MessageTreeRepository(session=cur_session) as msgtr, MsgTemplateRepository(session=cur_session) as mtr:
            allNode = msgtr.listAll({'deleted': 0})
            allNode.sort(key=lambda node: node.parent_id)
            # 树
            tree = self.__getTree(allNode)
            nodePath = []
            self.__get_node_path([tree], nodeId, nodePath)
            path = "/".join(str(path) for path in nodePath)
            msgs = mtr.listAllFuzzyByTreePath(path)
            # 判断树结构是否存在消息
            if len(msgs) > 0:
                raise MockFactoryDeleteTreeNodeFailHasMsg()
            else:
                self.__delete_node(msgtr, nodeId)

    def getNodePath(self, nodeId):
        """
        获取某个节点在树中的路径
        """
        cur_session = App().db.create_scoped_session()
        with MessageTreeRepository(session=cur_session) as mtr:
            allNode = mtr.listAll({'deleted': 0})
            allNode.sort(key=lambda node: node.parent_id)
            # 树
            tree = self.__getTree(allNode)
            nodePath = []
            self.__get_node_path([tree], nodeId, nodePath)
            return "/".join(str(path) for path in nodePath)

    def __addNode(self, tmpNode, node):
        """
        递归增加子节点
        """
        if tmpNode['id'] == node['parent_id']:
            tmpNode['children'].append(node)
            return
        else:
            for child in tmpNode['children']:
                self.__addNode(child, node)

    def __getTree(self, nodes):
        """
        根据查询出的树数据，转换成树嵌套结构
        """
        for tmp in nodes:
            node = Node(tmp.id, tmp.name, tmp.parent_id)
            if node.parent_id == 0:
                tmpNode = node.__dict__
            else:
                self.__addNode(tmpNode, node.__dict__)
        return tmpNode

    def __get_node_path(self, tree, id, path):
        """
        多叉树获取指定节点路径.
        """
        for node in tree:
            path.append(node['label'])
            if node['id'] == id:
                return path
            if 'children' in node.keys():
                result = self.__get_node_path(node['children'], id, path)
                if result:
                    return result
            path.pop()
        return None

    def __delete_node(self, r, node_id):
        r.update(node_id, {'deleted': time.time()})
        nodes = r.listAll({'parent_id': node_id, 'deleted': 0})
        for node in nodes:
            self.__delete_node(r, node.id)


class Node:

    def __init__(self, id, name, parent_id):
        self.id = id
        self.label = name
        self.parent_id = parent_id
        self.children = []

    def addChild(self, node):
        self.children.append(node)

    def keys(self):
        return ('id', 'label', 'parent_id', 'children')

    def __getitem__(self, item):
        return getattr(self, item)


if __name__ == '__main__':
    pass
