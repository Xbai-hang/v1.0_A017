# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: trie
@Description: 
@CreateTime: 2021/3/27
"""
from match.trie_node import TrieNode
from match.pattern import Pattern
from match.match_item import MatchItem
from match.match_node_info import MatchNodeInfo


class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    def clear(self):
        self.root.clear()

    def is_void(self):
        if self.root.sons and len(self.root.sons) > 0:
            return False
        return True

    def addPath(self, ps, ts):
        nowNode = self.root
        for p in ps:
            nowNode = nowNode.addSon(p)
        nowNode.update_obj(ts)

    def addPattern(self, pt):
        ts = []
        if pt.type == Pattern.Pattern_Short_Neighour:
            for t in pt.targets:
                ts.append(Pattern.add_neighnour_sign(t))
        else:
            ts.extend(pt.targets)
        self.addPath(pt.parts, ts)

    def judeAll(self, sen, start):
        nowNode = self.root
        objs = []
        for i in range(start, len(sen), 1):
            if nowNode.sons is None:
                return objs
            c = sen[i]
            nowNode = nowNode.sons.get(c)
            if nowNode is None:
                return objs
            if nowNode.obj:
                nowObj = nowNode.obj
                objs.append((nowObj, i + 1))
        return objs

    # 字符串全匹配
    def findAll(self, sen):
        ret = []
        i = 0
        while i < len(sen):
            objs = self.judeAll(sen, i)
            objs.sort(key=lambda x: x[1])
            if objs:
                ret.append((i, sen[i:objs[-1][1]], objs[-1][0]))
            i += 1
        # print('ret', ret)
        return ret

    # 正向最大匹配
    def find(self, sen):
        ret = []
        i = 0
        while i < len(sen):
            obj, j = self.judeLong(sen, i)
            if obj is not None:
                ret.append((i, sen[i:j], obj))
            else:
                j = i + 1
            i = j
        return ret

    # 完全匹配
    def find_whole(self, sen):
        ret = None
        i = 0
        while i < len(sen):
            obj, j = self.judeLong(sen, i)
            if obj is not None:
                if j == len(sen):
                    ret = obj
            else:
                j = i + 1
            i = j
        return ret

    # 字符串全匹配
    def findAll_(self, sen, limit):
        ret = []
        i = 0
        tn = 0
        while i < len(sen):
            objs = self.judeAll(sen, i)
            if len(objs) > 0:
                for obj, j in objs:
                    ret.append((i, sen[i:j], obj))
                tn += 1
                if tn > limit:
                    break
            i += 1
        # print('ret',ret)
        return ret

    def judeLong(self, sen, start):
        nowNode = self.root
        nowObj = None
        for i in range(start, len(sen), 1):
            if nowNode.sons is None: return nowObj, i
            c = sen[i]
            nowNode = nowNode.sons.get(c)
            if nowNode is None: return nowObj, i
            if nowNode.obj: nowObj = nowNode.obj
        return nowObj, len(sen)

    # 正向最大匹配
    def find_limit(self, sen, limit=0, max_len=1000000):
        if not sen: return []
        ret = []
        i = 0
        mlen = min(max_len, len(sen))
        while i < mlen:
            obj, j = self.judeLong(sen, i)
            if obj is not None:
                ret.append((i, sen[i:j], obj))
                if 0 < limit <= len(ret):
                    break
            else:
                j = i + 1
            i = j
        return ret

    def add_needs(self, match_node, need_item_nodes, new_needs):
        if not match_node.node.sons: return
        for p in match_node.node.sons:
            if p not in need_item_nodes: need_item_nodes[p] = []
            if match_node not in need_item_nodes[p]:
                need_item_nodes[p].append(match_node)
                new_needs.append((p, match_node))

    def add_item(self, item, obj, new_items, all_items, match_node_parent=None):
        for new_k in obj:
            is_neighnour = Pattern.is_neighnour_concept(new_k)
            # 如果要求相邻，去除相邻标志
            if is_neighnour:
                new_k = Pattern.remove_neighnour_sign(new_k)
            new_item = MatchItem(new_k)
            if match_node_parent:
                new_item.s = match_node_parent.s
            else:
                new_item.s = item.s
            new_item.e = item.e

            # 旧概念集合中已经包含，不要
            if MatchItem.contains(new_item, all_items.get(new_k)):
                continue

            # 新概念集合中已经包含，不要
            if MatchItem.contains(new_item, new_items):
                continue

            if match_node_parent:
                new_item.parts = match_node_parent.getParts()
            else:
                new_item.parts = []
            new_item.parts.append(item)

            # 模板要求相邻，但是概念不相邻，则概念不满足要求
            if is_neighnour and not new_item.is_son_neighbour():
                # print('not neighnour sons',new_item)
                continue
            new_items.append(new_item)

    # 非相邻排列匹配
    def match(self, items):
        all_items = {}
        if self.is_void():
            for item in items:
                k = item.key
                if k not in all_items:
                    all_items[k] = []
                # 已经处理过的item，不再处理
                if item in all_items[k]:
                    continue
                all_items[k].append(item)
            return all_items
        need_item_nodes = {}
        now_items = items
        while len(now_items) > 0:
            new_items = []
            new_needs = []
            for item in now_items:
                k = item.key
                if k not in all_items:
                    all_items[k] = []
                # 已经处理过的item，不再处理
                if item in all_items[k]:
                    continue
                all_items[k].append(item)
                mns = need_item_nodes.get(k)
                if mns:
                    removes = []
                    for i in range(len(mns)):
                        mn = mns[i]
                        mson = mn.node.get_son(k)
                        # 位置不对
                        if mn.e > item.s:
                            continue
                        if not mson:
                            continue
                        removes.append(i)
                        if mson.obj:
                            self.add_item(item, mson.obj, new_items, all_items, mn)
                        if mson.sons:
                            new_mn = MatchNodeInfo(mson, mn.s, item.e, item, mn)
                            self.add_needs(new_mn, need_item_nodes, new_needs)
                    for ii in range(len(removes) - 1, -1, -1):
                        i = removes[ii]
                        del mns[i]
                son = self.root.get_son(k)
                if son:
                    if son.obj:
                        self.add_item(item, son.obj, new_items, all_items)
                    if son.sons:
                        new_mn = MatchNodeInfo(son, item.s, item.e, item)
                        self.add_needs(new_mn, need_item_nodes, new_needs)
            while len(new_needs) > 0:
                tmp_new_needs = []
                for p, match_node in new_needs:
                    m_items = all_items.get(p)
                    if not m_items:
                        continue
                    minV = 10000
                    min_item = None
                    for item in m_items:
                        dv = item.s - match_node.e
                        if dv < 0:
                            continue
                        # 选择位置最近的
                        if dv < minV:
                            min_item = item
                            minV = dv
                    if not min_item:
                        continue
                    mson = match_node.node.get_son(p)
                    if not mson:
                        continue
                    if mson.obj:
                        self.add_item(item, mson.obj, new_items, all_items, match_node)
                    if mson.sons:
                        new_mn = MatchNodeInfo(mson, mn.s, item.e, item, mn)
                        self.add_needs(new_mn, need_item_nodes, tmp_new_needs)
                new_needs = tmp_new_needs
            now_items = new_items
        return all_items

    def __str__(self):
        ss = []
        self.root.items(ss)
        return '\t'.join(ss)
