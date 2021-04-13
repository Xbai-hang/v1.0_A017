# -*- coding: utf-8 -*-

"""
@Version: V1.0.0
@File: test
@Description: 
@CreateTime: 2021/4/5 16:25
"""

import json
from predictor import Predictor
from util.readRepositoryWords import readRepositoryWordsToList as read
# 语料列表

if __name__ == "__main__":
    # example_input = '{"document": [{"block_id": "0", "text": "08年4月，郑煤集团拟以非公开发行的方式进行煤炭业务整体上市，解决与郑州煤电同业竞争问题，但之后由于股市的大幅下跌导致股价跌破发行价而被迫取消整体上市。"}], "key": "79c29068d30a686", "qas": [[{"question": "中心词", "answers": [{"start_block": "0", "start": 57, "end_block": "0", "end": 58, "text": "导致", "sub_answer": "null"}]}]]}'
    # example_output = '{"document": [{"block_id": "0", "text": "08年4月，郑煤集团拟以非公开发行的方式进行煤炭业务整体上市，解决与郑州煤电同业竞争问题，但之后由于股市的大幅下跌导致股价跌破发行价而被迫取消整体上市。"}], "key": "79c29068d30a686", "qas": [[{"question": "原因中的核心名词", "answers": [{"start_block": "0", "start": 50, "end_block": "0", "end": 51, "text": "股市", "sub_answer": "null"}]}, {"question": "原因中的谓语或状态", "answers": [{"start_block": "0", "start": 53, "end_block": "0", "end": 56, "text": "大幅下跌", "sub_answer": "null"}]}, {"question": "中心词", "answers": [{"start_block": "0", "start": 57, "end_block": "0", "end": 58, "text": "导致", "sub_answer": "null"}]}, {"question": "结果中的核心名词", "answers": [{"start_block": "0", "start": 59, "end_block": "0", "end": 60, "text": "股价", "sub_answer": "null"}]}, {"question": "结果中的谓语或状态", "answers": [{"start_block": "0", "start": 61, "end_block": "0", "end": 65, "text": "跌破发行价", "sub_answer": "null"}]}]]}'
    example_input, example_output = [], []
    with open('./testJson/example_input.json', encoding='utf-8', mode='r') as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            example_input.append(line)
    with open('./testJson/example_output.json', encoding='utf-8', mode='r') as w:
        for line in w.readlines():
            line = line.replace('\n', '')
            example_output.append(line)
    count = [0, 0, 0]
    try:
        for index in range(len(example_input)):
            obj = Predictor()
            output = obj.predict(json.loads(example_input[index]))
            if output != json.loads(example_output[index]):
                print('预测失败')
                count[0] = count[0] + 1
            else:
                print('预测成功')
                count[1] += 1
            count[2] += 1
    except TypeError as Argument:
        print(Argument)
        pass
    finally:
        precision = count[1] / count[2]
        recall = count[1] / count[2]
        print('Total test example: ', count[2])
        print('Total succeed test example', count[1])
        print('Total failed test example', count[0])
        print('precision: {:.5f}%'.format(precision*100))
        print('recall: {:.5f}%'.format(recall*100))
