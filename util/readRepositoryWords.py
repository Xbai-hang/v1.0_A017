# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: readRepositoryWords
@Description: 
@CreateTime: 2021/4/2
"""


import os
from match.trie import Trie


def readRepositoryWordsToTrie(filePath: str, trie: Trie) -> None:
    """
    :param filePath: 词库文件路径
    :param trie: Trie树
    :return: None
    """
    fileName = os.path.basename(filePath).split('.')[0]
    with open(filePath, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            trie.addPath(line, fileName)
    return


def readRepositoryWordsToDict(filePath: str, dict_y: dict) -> None:
    """
    :param filePath: 词库文件路径
    :param dict_y: 因果词标签
    :return: None
    """
    with open(filePath, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            dict_y[line[0:-1]] = line[-1]
    return


def readRepositoryWordsToList(filePath: str, rule_list: list) -> None:
    """
    :param filePath: 词库文件路径
    :param rule_list: 句式列表
    :return: None
    """
    with open(filePath, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            rule_list.append(line)
    return
