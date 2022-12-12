from __future__ import division
import os
import sys
import time
import json
import argparse
from pathlib import Path

import logging

# 写入log
logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='./log.log',
                    filemode='w',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志, a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                    )


# 评估指标 无标记依存正确率（UAS）
def score(prefile, answerfile):
    with open(answerfile, 'r') as f1, open(prefile, 'r') as f2:
        answer = json.load(f1)
        predict = json.load(f2)

    a = b = 0
    for ans, pre in zip(answer, predict):
        adic = {}
        # 分词和支配词都要正确
        for d in ans['words']:
            adic[d['id']] = d['form'] + "-" + str(d['head'])
        a += len(adic)
        for p in pre['words']:
            if p['id'] not in adic:
                continue
            if (p['form'] + "-" + str(p['head'])) == adic.get(p['id']):
                b += 1

    if a == 0 or b == 0:
        UAS = 0
    else:
        UAS = b / a
    return round(UAS, 2)


def save_result(UAS):
    dic = {'UAS': UAS}
    with open('./output.json', 'w') as f:
        json.dump(dic, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    try:
        logging.info({
            "event_type": "EventType.TASK_STARTED",
            "message": "依存句法分析评测工具",
            "level": "info",
            "timestamp": time.strftime("%Y-%m-%dT %H:%M.%S", time.localtime())
        })

        parser = argparse.ArgumentParser(description='')
        parser.add_argument('--input', default='/input', help='Location of WIDERFACE root directory')
        parser.add_argument('--input_answer_path', default='/input_answer_path',
                            help='Location of WIDERFACE root directory')
        args = parser.parse_args()
        while len(sys.argv) > 1:
            sys.argv.pop()
        input_path = args.input
        input_answer_path = args.input_answer_path

        for file1 in Path(input_path).glob('**/*.json'):
            print(str(file1))
            for file2 in Path(input_answer_path).glob('**/*.json'):
                print(str(file2))
                if os.path.exists(file2):
                    UAS = score(file1, file2)
                    save_result(UAS)
                    logging.info('评估成功!!!   评估指标为 UAS:{}'.format(UAS))
                    print('评估成功!!!   评估指标为 UAS:{}'.format(UAS))

    except Exception as e:
        logging.error({
            "event_type": "EventType.TASK_CRASHED",
            "message": "整体文件错误",
            "level": "error",
            "timestamp": time.strftime("%Y-%m-%dT %H:%M.%S", time.localtime()),
            "extra": {
                "exc_info": e
            }
        })

