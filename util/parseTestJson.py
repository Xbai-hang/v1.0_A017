# -*- coding: utf-8 -*-

"""
@Version: V1.1.0
@File: parseTestJson
@Description: 解析多个官方给的样例类json文件中的json数据并合并
@CreateTime: 2021/3/27
"""
import json
import re
import os


def readJson(file: str):
    """
    处理官方的json文件
    :param file: 待处理文件的路径
    :return: 语料、因果词、主体、状态的存储列表
    """
    # 确保路径为绝对路径
    file = os.path.abspath(file)

    # 打开待处理json文件
    f = open(file, mode='r', encoding='utf-8')
    all_file = f.read()
    all_list = re.findall(r'{"document".+}', all_file)

    # 初始化语料、因果词、主体、状态の存储列表
    words_y = []
    words_z = []
    words_g = []
    words_t = []

    # 文本处理及保存
    for item in all_list:
        # 转为python 字典
        Dict = json.loads(item)
        words_y.append(Dict.get("document")[0].get("text") + '\n')

        # 获取 qas 键值列表
        qas_list = Dict.get("qas")[0]

        for res in qas_list:
            question_str = res.get("question")
            answers_list = res.get("answers")

            # 原因/结果中的核心名词
            if question_str in ('原因中的核心名词', '结果中的核心名词'):
                for req in answers_list:
                    words_z.append(req.get("text") + '\n')
            # 中心词
            elif question_str == '中心词':
                for req in answers_list:
                    words_g.append(req.get("text") + '\n')
            # 原因/结果中的谓语或状态
            elif question_str in ('原因中的谓语或状态', '结果中的谓语或状态'):
                for req in answers_list:
                    words_t.append(req.get("text") + '\n')
            else:
                continue

    # 关闭数据流
    f.close()

    return words_y, words_z, words_g, words_t


def subFile(first_file: str, second_file: str, save_path: str = os.getenv('Desktop')):
    """
    合并多个处理后的文件列表
    :param first_file: 待读取文件路径
    :param second_file: 待读取文件路径
    :param save_path: 处理结果文件存储路径
    :return: null
    """

    # 读取数据文件
    first_words_y, first_words_z, first_words_g, first_words_t = readJson(first_file)
    second_words_y, second_words_z, second_words_g, second_words_t = readJson(second_file)

    # 待存储数据列表
    words_y = first_words_y + second_words_y
    words_z = first_words_z + second_words_z
    words_g = first_words_g + second_words_g
    words_t = first_words_t + second_words_t

    # 数据处理(去重)
    words_y = list(set(words_y))
    words_g = list(set(words_g))
    words_z = list(set(words_z))
    words_t = list(set(words_t))

    # 打开存储文件
    fy = open(os.path.join(save_path, '语料.txt'), 'w+', encoding='utf-8')
    fz = open(os.path.join(save_path, '主体.txt'), 'w+', encoding='utf-8')
    fg = open(os.path.join(save_path, '因果词.txt'), 'w+', encoding='utf-8')
    ft = open(os.path.join(save_path, '状态.txt'), 'w+', encoding='utf-8')

    # 存储数据
    for item in words_y:
        fy.write(item)
    for item in words_z:
        fz.write(item)
    for item in words_g:
        fg.write(item)
    for item in words_t:
        ft.write(item)

    # 关闭文件流
    fy.close()
    fz.close()
    fg.close()
    ft.close()
    return
