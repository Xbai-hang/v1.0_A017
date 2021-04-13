# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: parseTestJson_old
@Description: 解析官方给的样例类json文件中的json数据
@CreateTime: 2021/3/23
"""


import json
import re
import os


def readJson(file: str, savePath: str):
    """
        处理官方json数据文件
        :param file: 文件路径
        :param savePath: 解析后txt文件存储路径
        :return: 无返回值
    """
    # 处理文件路径
    filePath = os.path.dirname(file)
    fileName = os.path.basename(file)

    # 打开待处理json文件
    f = open(os.path.join(filePath, fileName), encoding='utf-8')
    all_file = f.read()
    all_list = re.findall(r'{"document".+}', all_file)
    f.close()

    # 打开存储文件
    fy = open(os.path.join(filePath, '语料.txt'), 'w+', encoding='utf-8')
    fz = open(os.path.join(filePath, '主体.txt'), 'w+', encoding='utf-8')
    fg = open(os.path.join(filePath, '因果词.txt'), 'w+', encoding='utf-8')
    ft = open(os.path.join(filePath, '状态.txt'), 'w+', encoding='utf-8')

    # 初始化语料、因果词、主体、状态の存储列表
    words_z = []
    words_g = []
    words_t = []

    # 文本处理及保存
    for item in all_list:
        # 转为python 字典
        Dict = json.loads(item)
        fy.write(Dict.get("document")[0].get("text") + '\n')

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
                pass

    # 数据处理(去重)
    words_g = list(set(words_g))
    words_z = list(set(words_z))
    words_t = list(set(words_t))

    # 存储数据
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

