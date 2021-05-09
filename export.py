# -*- coding: utf-8 -*-
'''
   Project:       label_upload
   File Name:     export
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/5/9
   Software:      PyCharm
'''
import json

import argparse
import os

import requests
from tqdm import tqdm

import config

'''
导出已标记的语料
    1. 获取本次需要导出的所有项目id，手动指定或自动获取
    2. 发起get请求，获取标记结果
    3. 解析标记结果
    4. 存入tsv文件，文件格式如下
        | Path | StartTime/EndTime | Transcript |
'''

# get args
parser = argparse.ArgumentParser()
parser.add_argument("--id_file", default="./ids.tsv", help=None)
parser.add_argument("--output_file", default="./export_2021_05_09.tsv", help=None)

args = parser.parse_args()

def get_projects_id(file_path=None) -> list:
    '''
    根据文件获取要导出数据的项目id
    :param file_path: 包含项目id的tsv文件，\n为分隔符，可以为空，后续开发为自动请求api获取双重方式
    :return: 项目id列表
    '''
    with open(file_path, "r+", encoding="utf-8") as id_file:
        ids = [ids.strip() for ids in id_file.readlines()]
    return ids

def get_annotations(id) -> list:
    '''
    发起get请求，获取指定项目id的标记结果，转换为dict格式等待下一步解析
    :param ids: 指定项目id
    :return: 经过json解析的list，等待后续解析
    '''
    url = f"{config.Config.URL}/api/projects/{id}/export?exportType=JSON"
    headers = {"Authorization": f"Token {config.Config.TOKEN}"}
    res = json.loads(requests.get(url, headers=headers).text)

    return res

def analyze_and_save(raw_res: list, output_path: str):
    '''
    将获取到的标记结果进行解析，并存储为tsv文件，格式如上所述
    :param raw_res:
    :param output_path:
    :return:
    '''
    # res结构解析
        # 1. 标记结果：res[0]['annotations'][0]['result'][0]['value'] -> {'start': start_time, 'end': end_time, 'text': [label_text]}
        #　2. 路径：res[0]['data']['audio'] -> 'remote_path_prefix/file_name'

    if not os.path.exists(output_path):
        with open(output_path, "w+", encoding="utf-8") as out:
            out.write("PATH\tSTART_TIME/END_TIME\tTRANSCRIPT\n")

    with open(output_path, "a+", encoding="utf-8") as out:
        for elem in tqdm(raw_res, desc="[Analyzing]"):
            file_path = elem['data']['audio']
            file_start_time = elem['annotations'][0]['result'][0]['value']['start']
            file_end_time = elem['annotations'][0]['result'][0]['value']['end']
            try:
                transcripts = elem['annotations'][0]['result'][0]['value']['text'][0].strip()
            except Exception as e:
                transcripts = elem['annotations'][0]['result'][-1]['value']['text'][0].strip()

            # save
            print(f"{file_path}\t{file_start_time}/{file_end_time}\t{transcripts}", file=out, flush=False)


if __name__ == '__main__':
    ids = get_projects_id(args.id_file)
    for id in ids:
        raw_res = get_annotations(id)
        analyze_and_save(raw_res, args.output_file)
    print("All Done!")