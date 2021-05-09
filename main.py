# -*- coding: utf-8 -*-
'''
   Project:       label_upload
   File Name:     all_up
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/4/15
   Software:      PyCharm
'''
import argparse
import json
import threading
import time

import requests
from tqdm import tqdm

import config
from projectCreator import projects_creator
from upload_audio import upload

mutex = threading.Lock()

'''use multi-thead to upload datasets'''
parser = argparse.ArgumentParser()
parser.add_argument("--trans", default=r"E:\ChineseSpeechCorpus\xutangx\all_wav.lst", help="转录文本文件")
parser.add_argument("--src_prefix", default=r"E:\ChineseSpeechCorpus\xutangx\zxr", help="本地音频源文件路径前缀")
parser.add_argument("--remote_prefix", default=r"/data/local-files/?d=label-studio/data/xutangx/zxr", help="远端音频源文件路径前缀")
parser.add_argument("--threads", default=1, help="同时上传线程数")
parser.add_argument("--project_prefix", default="学堂在线", help="本次新建所有项目的前缀")
parser.add_argument("--projects", default="./test.tsv", help="要创建的项目主名称")
parser.add_argument("--start", default=856675, help="音频文件起始行")
parser.add_argument("--end", default=861675, help="音频文件结束行")
args = parser.parse_args()

def upload_thread(lines: list, log_file, projetc_id: int, project_name: str):
    for line in tqdm(lines, desc=project_name):
        line = line.split("\t")
        file_name = line[0][4:]
        transcript = line[1]
        remote_path = f"{args.remote_prefix}/{file_name}"
        project_id = projetc_id
        file_path = f"{args.src_prefix}\{file_name}"
        code, data = upload(path=remote_path, text=transcript, project_id=project_id, file_path=file_path)
        mutex.acquire()
        print(f"-----\nTread: {threading.current_thread().name}\nFile: {file_name}\nLabel: {transcript}Code: {code}\nData: {data}-----", file=log_file, flush=True)
        # print(f"-----\nTread: {threading.current_thread().name}\nFile: {file_name}\nLabel: {transcript}Code: {code}\nData: {data}-----")
        mutex.release()

def test():
    while True:
        print(threading.current_thread().name)

def show(lines: list):
    for line in lines:
        line = line.split("\t")
        file_name = line[0][4:]
        transcript = line[1]
        if file_name == "20210331_1377112567268384768.wav":
            print(transcript)

def run():
    '''main function'''
    # 创建项目
    projects_id = projects_creator(args.projects, args.project_prefix)
    # read transcript file
    with open(args.trans, "r+",  encoding="utf-8") as src:
        lines = src.readlines()

    # slice data
    total_lines = lines[args.start:args.end]

    # 计算每个人应该标记的任务量
    tasks_per_person = int(len(total_lines) / len(projects_id))

    # 进行任务上传
    for i in range(1, len(projects_id)+1):
        id = projects_id[i-1]
        project_name = json.loads(requests.get(f"{config.Config.URL}/api/projects/{id}/", headers={"Authorization": f"Token {config.Config.TOKEN}"}).text)['title']
        lines = total_lines[tasks_per_person*(i-1):tasks_per_person*i if i != len(projects_id) else None]

        # calculate step
        step_length = int(len(lines) / args.threads)

        # call threads
        threads = []
        log = open(config.Config.LOG_FILE, "a+", encoding="utf-8")
        for i in range(1, args.threads+1):
            start = step_length*(i-1)
            end = step_length*i if i != args.threads else None
            # print(f"s: {start}, e: {end}")
            if end:
                threads.append(threading.Thread(target=upload_thread, name=f"Thread-{i}", args=(lines[start:end], log, id, project_name)))
                # threads.append(threading.Thread(target=show, name=f"Thread-{i}", args=(lines[start:end],)))
            else:
                threads.append(threading.Thread(target=upload_thread, name=f"Thread-{i}", args=(lines[start:], log, id, project_name)))
                # threads.append(threading.Thread(target=show, name=f"Thread-{i}", args=(lines[start:end],)))

        print(
            f"############################################################",
            f'Current Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }',
            f'Current Epoch Indexes:  {args.start} to {args.end}',
            f'Current Project Name: {project_name}'
            f'############################################################',
            sep="\n", file=log
        )
        [t.start() for t in threads]
        [t.join() for t in threads]



if __name__ == '__main__':
    run()