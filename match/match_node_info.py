# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: match_node_info
@Description: 
@CreateTime: 2021/3/27
"""


class MatchNodeInfo(object):

    def getParentIndex(self):
        return self.parentIndex

    def setParentIndex(self, parentIndex):
        self.parentIndex = parentIndex

    def __init__(self, node, s, e, parent_item, parent_node_info=None):
        self.node = node
        self.s = s
        self.e = e
        self.parent_item = parent_item
        self.parent_node_info = parent_node_info

    def __eq__(self, other):
        if not other:
            return False
        if other.s == self.s and other.parent_item == self.parent_item and other.node == self.node:
            return True
        return False

    def addPart(self, parts, index):
        if index is not None:
            parts.insert(0, index)

    def getParts(self):
        parts = []
        now_parent_item = self.parent_item
        self.addPart(parts, now_parent_item)
        now_parent_node_info = self.parent_node_info
        while now_parent_node_info is not None:
            index = now_parent_node_info.parent_item
            self.addPart(parts, index)
            now_parent_node_info = now_parent_node_info.parent_node_info
        return parts
