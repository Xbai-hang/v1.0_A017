# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: model
@Description: 
@CreateTime: 2021/4/1
"""


import re
import copy
from match.trie import Trie
import util.readRepositoryWords as read


class Model:
    """
        自定义预测模型类
    """
    # ----------留疑，这个存储的是因果词做键名，标签tag_0 tag_1做键值的字典--------------
    __dict_y = {}
    __file = ['./data/rule_1.txt', './data/rule_2.txt', './data/rule_3.txt']
    __rule_first, __rule_second, __rule_third = [], [], []
    __slots__ = ('word_y', 'site_y', 'parse_z', 'parse_l', 'parse_t', 'parse_f', 'sentence')

    def __init__(self, word_y: str, site_y_start: int, parse_z: list, parse_l: list, parse_t: list, parse_f: list, sentence: str, dict_y: dict):
        """
        :param word_y: 因果词
        :param site_y_start: 因果词起始位置
        :param parse_z: 主体列表
        :param parse_l: 连词列表
        :param parse_t: 状态列表
        :param parse_f: 分界词列表
        :param sentence: 语料
        :param dict_y: 因果词标签键值对
        """
        self.word_y = word_y
        self.site_y = site_y_start
        self.parse_z = parse_z
        self.parse_l = parse_l
        self.parse_t = parse_t
        self.parse_f = parse_f
        self.sentence = sentence
        self.__set_dict_y(dict_y)
        self.__set_all_rule_list()

    @staticmethod
    def __set_dict_y(dict_y: dict) -> None:
        """
        初始化因果词字典,键名:因果词,键值:tag_1\n
        :param dict_y: 字典
        :return: None
        """
        Model.__dict_y = dict_y

    @staticmethod
    def __set_all_rule_list() -> None:
        """
        初始化句式列表\n
        :return: Node
        """
        read.readRepositoryWordsToList(Model.__file[0], Model.__rule_first)
        read.readRepositoryWordsToList(Model.__file[1], Model.__rule_second)
        read.readRepositoryWordsToList(Model.__file[2], Model.__rule_third)

    # 因果词+结果+原因 对应fun1
    def __to_result_reason(self):
        # 所有待取主体列表/连词列表
        z_all = []
        t_all = []
        l_all = []
        # 遍历 所有抽取到的主体列表,抽取满足条件的主体
        for item in self.parse_z:
            if item[0] > self.site_y:
                z_all.append(item)
        # 遍历 所有抽取到的连词列表,抽取满足条件的连词
        for item in self.parse_l:
            if item[0] > self.site_y:
                l_all.append(item)
        # 遍历 所有抽取到的状态列表，抽取满足条件的状态
        for item in self.parse_t:
            if item[0] > self.site_y:
                t_all.append(item)
        # 声明需要抽取的原因/结果主体列表
        z_reason_all = []
        z_result_all = [z_all[0]]
        t_reason_all = []
        t_result_all = []
        # 放入结果列表中
        count_item: int = 1
        for item in l_all:
            if item[0] + len(item[1]) == z_all[count_item][0]:
                z_result_all.append(z_all[count_item])
                count_item = count_item + 1
            else:
                break
        # 将抽取出来的整个主体位置关系与主体语料都放入原因列表中
        if count_item < len(z_all):
            z_reason_all.append(z_all[count_item])
            count_item = count_item + 1
            for item in l_all[count_item - 2:]:
                if count_item >= len(z_all):
                    break
                if item[0] + len(item[1]) == z_all[count_item][0]:
                    z_reason_all.append(z_all[count_item])
                    count_item = count_item + 1
                else:
                    break
        # 分界词
        boundary: list = []
        for item in self.parse_f:
            if (item[0] > self.site_y) and (item[0] < z_reason_all[0][0]):
                boundary = item
                break
        count_zt: int = 0
        # 抽取出结果状态
        if z_result_all is None:
            count_xx: int = 0
            t_result_all.append(t_all[0])
            for item in l_all[1::]:
                if t_result_all[count_xx][0] + len(t_result_all[count_xx][1]) == item[0] and item[0] < boundary[0]:
                    t_result_all.append(item)
        else:
            # 在第一个结果主体和分界词中间的所有状态都提取出来
            for item in t_all:
                if (item[0] > z_result_all[count_zt][0]) and (item[0] < boundary[0]):
                    t_result_all.append(item)
        # 抽取出原因状态
        if z_reason_all is None:  # 在分界词后面的第一个状态（或者根据连词进行连接判断)   XXXXXXXX 未实现 XXXXXXX
            for item in t_all:
                if item[0] > self.site_y:
                    t_reason_all.append(item)
                    break
        else:
            # 最后一个结果词后的状态如果满足状态的语序<=最后一个原因主体语序+原因主体长度+2则提取出来作为原因状态
            for item in t_all:
                if (item[0] > boundary[0]) and (item[0] > z_reason_all[0][0]) and (item[0] < z_reason_all[-1][0]):
                    t_reason_all.append(item)
                if (item[0] > z_reason_all[-1][0]) and ((z_reason_all[-1][0] + len(z_reason_all[-1][1]) + 2) > item[0]):
                    t_reason_all.append(item)
        return z_reason_all, t_reason_all, z_result_all, t_result_all

    # 因果词+原因+结果 对应fun2
    def __to_reason_result(self):
        # 所有待取主体列表/连词列表
        z_all = []
        l_all = []

        # 遍历 所有抽取到的主体列表,抽取满足条件的主体
        for item in self.parse_z:
            if item[0] > self.site_y:
                z_all.append(item)

        # 遍历 所有抽取到的连词列表,抽取满足条件的连词
        for item in self.parse_l:
            if item[0] > self.site_y:
                l_all.append(item)

        # 声明需要抽取的原因/结果主体列表
        z_reason_all = [z_all[0][1]]
        z_result_all = []

        # 放入结果列表中
        count_item: int = 1
        for item in l_all:
            if item[0] + len(item[1]) == z_all[count_item][0]:
                z_reason_all.append(z_all[count_item][1])
                count_item = count_item + 1
            else:
                break

        # 放入原因列表中
        if count_item < len(z_all):
            z_result_all.append(z_all[count_item][1])
            count_item = count_item + 1
            for item in l_all[count_item - 2:]:
                if count_item >= len(z_all):
                    break
                if item[0] + len(item[1]) == z_all[count_item][0]:
                    z_result_all.append(z_all[i][1])
                    i = i + 1
                else:
                    break
        print("fun2原因主体:{}".format(z_reason_all))
        print("fun2结果主体:{}".format(z_result_all))
        return z_reason_all, [], z_result_all, []

    # 结果+因果词+原因 对应fun3
    def __result_to_reason(self):
        # 原因/结果主体列表
        z_reason, z_result = [], []
        # 原因/结果状态列表
        t_reason, t_result = [], []

        # 因果词前后的主体列表
        z_all_front, z_all_rear = [], []
        # 因果词前后的连词列表
        l_all_front, l_all_rear = [], []
        t_all_front, t_all_rear = [], []

        # 遍历主体列表分割前后
        for item in self.parse_z:
            if item[0] < self.site_y:
                z_all_front.append(item)
            else:
                z_all_rear.append(item)
        # 遍历连词列表分割前后
        for item in self.parse_l:
            if item[0] < self.site_y:
                l_all_front.append(item)
            else:
                l_all_rear.append(item)
        # 遍历状态列表分割前后
        for item in self.parse_t:
            if item[0] < self.site_y:
                t_reason.append(item[1])
            else:
                t_result.append(item[1])

        # 将因果词前的主体提取出来作为结果主体列表
        if len(z_all_front):
            count_z_front: int = len(z_all_front) - 1
            z_result.append(z_all_front[count_z_front][1])
            count_z_front -= 1
            l_all_front.reverse()
            for item in l_all_front:
                if count_z_front < 0:
                    break
                if z_all_front[count_z_front + 1][0] - len(item[1]) == item[0]:
                    z_result.append(z_all_front[count_z_front][1])
                    count_z_front -= 1
                else:
                    # print(count_z_front)
                    break

        # 将因果词后的主体提取出来作为原因主体列表
        if len(z_all_rear):
            count_z_rear: int = 1
            z_reason.append(z_all_rear[0][1])
            for item in l_all_rear:
                if count_z_rear >= len(z_all_rear):
                    break
                if item[0] + len(item[1]) == z_all_rear[count_z_rear][0]:
                    z_reason.append(z_all_rear[count_z_rear][1])
                    count_z_rear = count_z_rear + 1
                else:
                    break
        return z_reason, t_reason, z_result, t_result

    # 原因+结果+因果词 对应fun4
    def __reason_to_result(self):
        print('fun4')
        return [], [], [], []

    # 无句式简单处理
    def __no__(self):
        # 原因/结果主体列表
        z_reason, z_result = [], []
        # 因果词前后的主体列表
        z_all_front, z_all_rear = [], []
        # 因果词前后的连词列表
        l_all_front, l_all_rear = [], []
        # 原因状态/结果状态
        t_reason, t_result = [], []
        for item in self.parse_z:
            if item[0] < self.site_y:
                z_all_front.append(item)
            else:
                z_all_rear.append(item)
        for item in self.parse_l:
            if item[0] < self.site_y:
                l_all_front.append(item)
            else:
                l_all_rear.append(item)

        # 将因果词前的主体提取出来作为原因主体列表
        if len(z_all_front):
            count_z_front: int = len(z_all_front) - 1
            z_reason.append(z_all_front[count_z_front])
            count_z_front -= 1
            # print(len(l_all_front))
            l_all_front.reverse()
            for item in l_all_front:
                if count_z_front < 0:
                    break
                if z_all_front[count_z_front + 1][0] - len(item[1]) == item[0]:
                    z_reason.append(z_all_front[count_z_front])
                    count_z_front -= 1
                else:
                    # print(count_z_front)
                    break
        if len(z_all_rear):
            count_z_rear: int = 1
            z_result.append(z_all_rear[0])
            for item in l_all_rear:
                if count_z_rear >= len(z_all_rear):
                    break
                if item[0] + len(item[1]) == z_all_rear[count_z_rear][0]:
                    z_result.append(z_all_rear[count_z_rear])
                    count_z_rear = count_z_rear + 1
                else:
                    break
        if z_reason:
            pre_site = z_reason[0][0]
            for item in z_reason[1:]:
                for t in self.parse_t:
                    if (pre_site < t[0]) and (t[0] < item[0]):
                        t_reason.append(t)
                        break
                pre_site = item[0]
            last_site = z_reason[-1][0]
            for t in self.parse_t:
                if (last_site < t[0]) and (t[0] < self.site_y):
                    t_reason.append(t)
        else:
            pre_site = 0
            flag = False
            self.parse_t.reverse()
            for item in self.parse_t:
                if flag:
                    if pre_site - item[0] - len(item[1]) <= 2:
                        t_reason.append(item)
                        pre_site = item[0]
                if item[0] < self.site_y:
                    pre_site = item[0]
                    t_reason.append(item)
                    flag = True
            self.parse_t.reverse()

        if z_result:
            pre_site = z_result[0][0]
            for item in z_result[1:]:
                for t in self.parse_t:
                    if (pre_site < t[0]) and (t[0] < item[0]):
                        t_result.append(t)
                        break
                pre_site = item[0]
            last_site = z_result[-1][0]
            for item in self.parse_t:
                if item[0] > last_site:
                    t_result.append(item)
                    break
        else:
            pre_site = 0
            flag = False
            for item in self.parse_t:
                if flag:
                    if item[0] - pre_site <= 2:
                        t_result.append(item)
                        pre_site = item[0] + len(item[1])
                if item[0] > self.site_y:
                    pre_site = item[0] + len(item[1])
                    t_result.append(item)
                    flag = True
        return z_reason, t_reason, z_result, t_result

    # main function
    def getAllWords(self):
        tag_1 = self.__dict_y.get(self.word_y, False)
        if tag_1 and tag_1 == '0':
            pass
        elif tag_1 and tag_1 == '1':
            mark_is_match = False
            for item in Model.__rule_first:
                pattern = item.split(' ')[0]
                tag_2 = item.split(' ')[1]
                match = re.match(pattern, self.sentence)
                # 匹配到句式
                if match is not None:
                    mark_is_match = True
                    if tag_2 == '1':
                        return self.__to_result_reason()
                    elif tag_2 == '2':
                        return self.__to_reason_result()
                    elif tag_2 == '3':
                        return self.__result_to_reason()
                    elif tag_2 == '4':
                        return self.__reason_to_result()

            # 未匹配到句式,简单处理
            if not mark_is_match:
                # print("未匹配到句式")
                return self.__to_reason_result()

        elif tag_1 and tag_1 == '2':
            mark_is_match = False
            for item in Model.__rule_second:
                pattern = item.split(' ')[0]
                tag_2 = item.split(' ')[1]
                match = re.match(pattern, self.sentence)
                # 匹配到句式
                if match is not None:
                    mark_is_match = True
                    if tag_2 == '1':
                        return self.__to_result_reason()
                    elif tag_2 == '2':
                        return self.__to_reason_result()
                    elif tag_2 == '3':
                        return self.__result_to_reason()
                    elif tag_2 == '4':
                        return self.__reason_to_result()
            # 未匹配到句式,简单处理
            if not mark_is_match:
                # print("未匹配到句式")
                return self.__result_to_reason()

        elif tag_1 and tag_1 == '3':
            # 标记是否匹配到句式
            mark_is_match = False
            for item in Model.__rule_third:
                pattern = item.split(' ')[0]
                tag_2 = item.split(' ')[1]
                match = re.match(pattern, self.sentence)

                # 匹配到句式
                if match is not None:
                    mark_is_match = True
                    if tag_2 == '1':
                        return self.__to_result_reason()
                    elif tag_2 == '2':
                        return self.__to_reason_result()
                    elif tag_2 == '3':
                        return self.__result_to_reason()
                    elif tag_2 == '4':
                        return self.__reason_to_result()
            # 未匹配到句式,简单处理
            if not mark_is_match:
                # print(r'未匹配到句式')
                return self.__no__()
        else:
            # LTP
            pass
