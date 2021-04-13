# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: predicate
@Description: 
@CreateTime: 2021/3/27
"""

import json
import copy
import functools
from model.model import Model
from match.trie import Trie
import util.readRepositoryWords as read


class Predictor:
    # 词库存储位置列表
    __dict_y, __cpm_questions = {}, {'原因中的核心名词': 1, '原因中的谓语或状态': 2, '中心词': 3, '结果中的核心名词': 4, '结果中的谓语或状态': 5}
    __file, __questions = ['./data/因果词.txt', './data/主体.txt', './data/连词.txt', './data/状态.txt', './data/分界词.txt'], [
        '原因中的核心名词', '原因中的谓语或状态', '结果中的核心名词', '结果中的谓语或状态']
    __z_trie, __l_trie, __t_trie, __f_trie = Trie(), Trie(), Trie(), Trie()

    def __init__(self):
        """
            初始化模型、配置
        """
        self.__initTrie__()

    @staticmethod
    def __initTrie__():
        # 生成Trie树
        read.readRepositoryWordsToDict(Predictor.__file[0], Predictor.__dict_y)
        read.readRepositoryWordsToTrie(Predictor.__file[1], Predictor.__z_trie)
        read.readRepositoryWordsToTrie(Predictor.__file[2], Predictor.__l_trie)
        read.readRepositoryWordsToTrie(Predictor.__file[3], Predictor.__t_trie)
        read.readRepositoryWordsToTrie(Predictor.__file[4], Predictor.__f_trie)

    @staticmethod
    def predict(content: dict) -> dict:
        """
        输入标注格式，已转为dict
        输出同标注格式，dict格式
        :param content: 标注格式，见样例:
        :return str:
        """
        # ------------------------需要处理content----------------------
        sentence = content['document'][0]['text']
        answers = content['qas'][0]
        y_list = answers[0]['answers'][0]
        site_y_start = y_list['start']
        word_y = y_list['text']
        # print(sentence + '\n' + word_y)
        parse_z = Predictor.__z_trie.findAll(sentence)
        parse_l = Predictor.__l_trie.findAll(sentence)
        parse_t = Predictor.__t_trie.findAll(sentence)
        parse_f = Predictor.__f_trie.findAll(sentence)
        pre_model = Model(word_y, site_y_start, parse_z, parse_l, parse_t, parse_f, sentence, Predictor.__dict_y)
        for index, item in enumerate(pre_model.getAllWords()):
            answer = Predictor.__write_json(item, Predictor.__questions[index])
            answers.append(answer)
        answers.sort(key=functools.cmp_to_key(Predictor.__cmp_answers))
        return content

    @staticmethod
    def __write_json(parse_all: list, question: str) -> dict:
        """
        向给定的dict中写入数据
        :param parse_all: 模型预测处理后返回的主体、状态列表
        :param question: 列表对应的类型说明,如结果中的谓语或状态等
        :return: 返回一个dict对象,是处理好的字典数据
        """
        qas = {"question": question, "answers": []}
        for item in parse_all:
            answer = {"start_block": "0", "start": item[0], "end_block": "0", "end": item[0] + len(str(item[1])) - 1, "text": str(item[1]), "sub_answer": None}
            qas['answers'].append(answer)
        return qas

    @staticmethod
    def __cmp_answers(dict1: dict, dict2: dict):
        """
        对answers列表的排序算法
        :param dict1: 列表中的字典元素1
        :param dict2: 列表中的字典元素2
        :return:
        """
        str1, str2 = dict1['question'], dict2['question']
        return 1 if (Predictor.__cpm_questions[str1] - Predictor.__cpm_questions[str2]) >= 0 else -1
