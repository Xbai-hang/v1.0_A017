# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: trie_node
@Description: 
@CreateTime: 2021/3/27
"""
import copy


class TrieNode(object):

    def __init__(self, obj=None):
        self.obj = obj
        self.sons = None

    def addSon(self, s, obj=None):
        if self.sons is None: self.sons = {}
        son = self.sons.get(s)
        if not son:
            son = TrieNode(obj)
            self.sons[s] = son
        else:
            son.update_obj(obj)
        return son

    def get_son(self, p):
        if not self.sons: return None
        return self.sons.get(p)

    def update_obj(self, obj):
        if obj is None: return
        if obj == self.obj: return
        new_obj = copy.deepcopy(obj)
        # print('obj',self.obj)
        # print('add_obj', new_obj)
        if self.obj is None:
            self.obj = new_obj
        else:
            if type(self.obj) == list:
                if type(new_obj) == list:
                    for ne in new_obj:
                        if ne not in obj: obj.append(ne)
                else:
                    if new_obj not in self.obj: self.obj.append(new_obj)
            else:
                if type(new_obj) == list:
                    if self.obj not in new_obj: new_obj.append(self.obj)
                    self.obj = new_obj
                else:
                    tmp = [self.obj, new_obj]
                    self.obj = tmp
        # print('new_obj',self.obj)

    def items(self, ss, prefix=''):
        if self.sons:
            ss.append("\n" + prefix)
            for s, son in self.sons.items():
                ss.append(str(s))
                son.items(ss, prefix + '\t')
                ss.append("\n" + prefix)
        if self.obj: ss.append('=>' + str(self.obj))

    def clear(self):
        if self.obj: self.obj = None
        if self.sons:
            self.sons.clear()
