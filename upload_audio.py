# -*- coding: utf-8 -*-
# @Time  : 2021/4/15 11:39
# @Author : lovemefan
# @File : upload_audio.py
import json
import os
import re
import wave

import requests

import config


def upload(path: str, text: str, project_id: int, file_path: str):
    url = f"{config.Config.URL}/api/projects/{project_id}/import"
    headers = {"Authorization": f"Token {config.Config.TOKEN}", "Content-Type": "application/json"}
    start = 0.0
    end = get_file_duration(file_path)
    # end = 3.922051886792453

    data = {
        "predictions": [
            {
                "result": [
                    {
                        "value": {
                            "start": start,
                            "end": end,
                            "text": [
                                text
                            ]
                        },
                        "from_name": "transcription",
                        "to_name": "audio",
                        "type": "textarea"
                    }
                ]
            }
        ],
        "data": {
            "audio": path
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response, data


def get_file_duration(path):
    """
    获取单个wav文件时长
    :param path: 文件路径
    :return:
    """
    with wave.open(path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
    return wav_length


if __name__ == '__main__':
    result = upload('/data/local-files/?d=label-studio/data/xutangx/zxr/20210331_1377111840626188289.wav', '在它从原始社会最初产生的时候', 4)
    print(result.text)
