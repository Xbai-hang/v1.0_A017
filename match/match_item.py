# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: match_item
@Description: 
@CreateTime: 2021/3/27
"""


class MatchItem(object):

    def __init__(self, key, s=0, e=0):
        self.key = key
        self.s = s
        self.e = e
        self.parts = None

    # 检测儿子节点内部是否首尾相连
    def is_son_neighbour(self):
        if not self.parts: return True
        for i in range(1, len(self.parts), 1):
            if self.parts[i].s != self.parts[i - 1].e: return False
        return True

    @staticmethod
    def contains(item, items):
        if not items: return False
        hasS = False
        hasE = False
        for it in items:
            if it.key != item.key: continue
            if it.s == item.s: hasS = True
            if it.e == item.e: hasE = True
        if not hasS or not hasE: return False
        return True

    def __eq__(self, other):
        if not other: return False
        if other.key == self.key and other.s == self.s and other.e == self.e:
            return True
        return False

    def __str__(self):
        s = str(self.key) + "\t(" + str(self.s) + "," + str(self.e) + ')'
        if self.parts:
            s += '\t{'
            for son in self.parts:
                s += str(son) + "\t"
            s += '\t}'
        return s

    def out_str(self, text):
        if not self.parts: return text[self.s:self.e]
        s = ''
        # lastPmi = None
        for pmi in self.parts:
            # if lastPmi and lastPmi.e < pmi.s:s += ' '
            s += ' '
            s += pmi.out_str(text)
            # lastPmi = pmi
        return s
