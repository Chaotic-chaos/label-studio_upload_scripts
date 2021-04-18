# -*- coding: utf-8 -*-
'''
   Project:       label_upload
   File Name:     projectCreator
   Author:        Chaos
   Email:         life0531@foxmail.com
   Date:          2021/4/17
   Software:      PyCharm
'''
import json

import requests

import config

'''读取预定义tsv文件，根据预定义项目名称创建项目'''


def projects_creator(path: str, name_prefix: str="") -> list:
    '''
    读取预定义的tsv文件，根据预定义项目名称创建项目；tsv文件中项目名称以\n分隔
    :param path: tsv文件路径; name_prefix: 名称前缀，默认为空
    :return: 所有项目的id
    '''
    # 读取tsv文件
    with open(path, "r+", encoding="utf-8") as f:
        names = f.readlines()
        names = [name.strip() for name in names]
    projects_id = []
    for name in names:
        url = f"{config.Config.URL}/api/projects"
        headers = {"Authorization": f"Token {config.Config.TOKEN}", "Content-Type": "application/json"}
        data = {
            "title": f"{name_prefix} - {name}",
            "description": config.Config.PROJETCS_DESP,
            "label_config": config.Config.LABEL_CONFIG,
            "expert_instruction": None,
            "show_instruction": False,
            "show_skip_button": True,
            "enable_empty_annotation": False,
            "show_annotation_history": True,
            "organization": None,
            "color": "",
            "maximum_annotations": 1,
            "is_published": True,
            "model_version": "",
            "is_draft": False,
            "min_annotations_to_start_training": 0,
            "show_collab_predictions": True,
            "sampling": None,
            "show_ground_truth_first": True,
            "show_overlap_first": True,
            "overlap_cohort_percentage": 0,
            "task_data_login": None,
            "task_data_password": None,
            "control_weights": None
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(data))
        # print(res)
        if res.status_code ==  201:
            # 创建成功
            projects_id.append(json.loads(res.text)["id"])
        else:
            with open(config.Config.LOG_FILE, "a+", encoding="utf-8") as log:
                print(f"-----Error Start-----\nTask {name}创建失败\n-----Error End-----", file=log, flush=True)
    return projects_id

if __name__ == '__main__':
    print(projects_creator("./projects.tsv", "学堂在线"))