# -*- coding:utf-8 -*-
# @Time: 2024/5/8 10:09
# @Author: huizhuo
# @Site： www.swust.edu.cn
# @Email: huizhuoli@foxmail.com
# @File: gen.py
# @Version V1.0.0

from http import HTTPStatus

import dashscope
import csv
import asyncio
import re
import json
import os

dashscope.api_key = "sk-f5bbcc489123418cb5a88e88a41652f2"

data = {
    "point": "职业道德",
    "point_id": "1",
    "question_type": "单选题",
    "qeustion_id": "1-1",
    "question": "职业道德的特征是什么？",
    "answer": "A",
    "options": {
        "A": "正直、诚实、守信、敬业",
        "B": "正直、诚实、守信、敬业、勤奋",
    },
    "prompt": "",
    "analysis": "答案分析"
}

Question_Type = {
    "Single": "单选题",
    "Multi": "多选题",
    "Judge": "判断题",
}

async def load_data_point(file_path):
    """
    加载知识点数据
    :return:
    """
    with open("../resources/QA_point.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for index,value in list(enumerate(Question_Type.values())):
                question_config = {
                    'question_type': Question_Type['Single'],
                    'question_id': row["题号"],
                    'point': row['知识点'],
                    'point_id': row['题号'],
                }
                if value == "多选题":
                    question_config['prompt'] = '帮忙出{}道关于{}的五个选项的多选题，格式为题目1，题目2等，并给出正确答案，并提供简洁的解析，输出格式为纯文本'.format( int(row['多选题'])*2 + 1,row['提问'])
                    question_config['question_type'] = Question_Type['Multi']
                elif value == "单选题":
                    question_config['prompt'] = '帮忙出{}道关于{}的单选题，并给出正确答案，并提供简洁的解析，输出格式为纯文本'.format(int(row['单选题'])*2, row['提问'])
                    question_config['question_type'] = Question_Type['Single']
                else:
                    question_config['prompt'] = '帮忙出{}道关于{}的判断题，并给出正确答案，并提供简洁的解析，输出格式为纯文本'.format(int(row['判断题'])*2, row['提问'])
                    question_config['question_type'] = Question_Type['Judge']

                print(question_config['prompt'])

                await gen_question(question_config)


def parsed_judge_response(question_config, content):

    question_blocks = re.split(r'\n\n\d*\. ', content)

    data_list = []

    for i, question_block in enumerate(question_blocks, start=1):
        # 提取问题
        question = question_block.split('\n')[0]
        try:
            answer_analysis = question_block.split('\n')[1]
        except IndexError:
            answer_analysis = ""

        answers = re.findall(r'答案：(.*?)(?=。|$)', answer_analysis, re.DOTALL)
        try:
            # 尝试分割并获取第二部分
            analysis = answer_analysis.split('。')[1]
        except IndexError:
            # 如果出现IndexError（索引错误），则设置analysis为空字符串
            analysis = ""

        try:
            # 尝试分割并获取第二部分
            ans = answers[0],
        except IndexError:
            # 如果出现IndexError（索引错误），则设置analysis为空字符串
            ans = ""
        # 构建data
        data = {
            "point": question_config['point'],
            "point_id": question_config['point_id'],
            "question_type": question_config['question_type'],
            "question_id": "{}_{}".format(question_config['question_id'], i + 10),
            "question": question,
            "answer": ans,
            "prompt": question_config['prompt'],
            "analysis": analysis,
        }
        data_list.append(data)
    print(data_list)
    save_question_file(data_list, "../resources/QA.csv")
    save_question_json(data_list, "../resources/QA.json")
    # print(data_list)


def parsed_multi_choice_response(question_config, content):

    # Parse the question and answer
    # 使用正则表达式分割题目
    question_blocks = re.split(r"\n\n题目\d+：", content)

    # 移除第一个空元素（如果存在）
    if question_blocks[0].strip() == "":
        question_blocks.pop(0)

    # 定义正则表达式模式
    question_pattern = re.compile(r"^(.+?)?\n")
    options_pattern = re.compile(r"([A-E]\. .+?)(?=\n[A-E]|\n\n(?:正确答案|答案)|$)", re.DOTALL)
    answer_pattern = re.compile(r"[\s\S]*答案：([A-E, ]+)")
    analysis_pattern = re.compile(r"[\s\S]*解析：(.+)")
    data_list = []
    json_list = []
    # 提取每个题目的信息
    for i, block in enumerate(question_blocks, start=1):
        # 提取问题
        question_match = question_pattern.search(block)
        question = question_match.group(1).strip() if question_match else None

        # 提取选项
        options_matches = options_pattern.findall(block)
        options = {match[0]: match[3:] for match in options_matches}

        # 提取答案
        answer_match = answer_pattern.search(block)
        answer = answer_match.group(1).strip() if answer_match else None

        # 提取解析
        analysis_match = analysis_pattern.search(block)
        analysis = analysis_match.group(1).strip() if analysis_match else None

        data = {
            "point": question_config['point'],
            "point_id": question_config['point_id'],
            "question_type": question_config['question_type'],
            "question_id": "{}_{}".format(question_config['question_id'], i + 5),
            "question": question,
            "answer": answer,
            "options": options,
            "prompt": question_config['prompt'],
            "analysis": analysis,
        }

        # 扁平化结构，将选项并入到主字典中
        flattened_data = {
            "point": data["point"],
            "point_id": data["point_id"],
            "question_type": data["question_type"],
            "question_id": data["question_id"],
            "question": data["question"],
            "answer": data["answer"],
            "prompt": data["prompt"],
            "analysis": data["analysis"]
        }

        # 将选项扁平化，直接添加到flattened_data字典中
        for option_key, option_value in data["options"].items():
            flattened_data[f"option_{option_key}"] = option_key + ':' + option_value
        # 添加到列表
        data_list.append(flattened_data)
        json_list.append(data)
    print(data_list)
    save_question_file(data_list, "../resources/QA.csv")
    save_question_json(json_list, "../resources/QA.json")



def parsed_choice_response(question_config, content):

    # 正则表达式，用于分割问题、选项、答案和解析
    question_pattern = re.compile(r'(\d+)\.\s(.+?)(?=\n\n\d+\.|\n{2,}$)', re.DOTALL)
    option_pattern = re.compile(r'([ABCD])\.\s+(.+)')

    # 分割整个内容到各个问题
    questions = question_pattern.findall(content)
    answer_pattern = re.compile(r'\s*\**答案[:：]\s*\**([A-E,\s]+)')
    analysis_pattern = re.compile(r'解析[:：](.*?)(?=\n\n\d+\.|\n{2,}$)', re.DOTALL)

    data_list = []
    json_list = []
    for i, (num, question_block) in enumerate(questions):
        # 提取选项
        options = dict(option_pattern.findall(question_block))
        answer_match = answer_pattern.search(question_block)
        analysis_match = analysis_pattern.search(question_block)
        answer = answer_match.group(1) if answer_match else None
        analysis = analysis_match.group(1).strip() if analysis_match else None

        data = {
            "point": question_config['point'],
            "point_id": question_config['point_id'],
            "question_type": question_config['question_type'],
            "question_id": "{}_{}".format(question_config['question_id'], i + 1),
            "question": question_block.split('\n')[0],
            "answer": answer,
            "options": options,
            "prompt": question_config['prompt'],
            "analysis": analysis,
        }

        # 扁平化结构，将选项并入到主字典中
        flattened_data = {
            "point": data["point"],
            "point_id": data["point_id"],
            "question_type": data["question_type"],
            "question_id": data["question_id"],
            "question": data["question"],
            "answer": data["answer"],  # 移除答案中的空格和换行符
            "prompt": data["prompt"],
            "analysis": data["analysis"]
        }

        # 将选项扁平化，直接添加到flattened_data字典中
        for option_key, option_value in data["options"].items():
            flattened_data[f"option_{option_key}"] = option_key + ':' + option_value
        # 添加到列表
        data_list.append(flattened_data)
        json_list.append(data)
    print(data_list)
    save_question_file(data_list, "../resources/QA.csv")
    save_question_json(json_list, "../resources/QA.json")

def save_question_file(data, csv_filename):
    """
    保存题目文件
    :param data:
    :param file_name:
    :return:
    """
    write_header = not os.path.exists(csv_filename)
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        # 确定CSV的列名
        fieldnames = ['point','point_id','question_type', 'question_id','question', 'answer','option_A', 'option_B', 'option_C', 'option_D','option_E', 'prompt', 'analysis' ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果是新文件，写入表头
        if write_header:
            writer.writeheader()
        # 写入数据
        for entry in data:
            writer.writerow(entry)

def save_question_json(data, json_filename):
    # 读取现有的JSON文件内容
    existing_data = []
    if os.path.exists(json_filename):
        with open(json_filename, 'r', encoding='utf-8') as jsonfile:
            try:
                existing_data = json.load(jsonfile)
            except json.JSONDecodeError:
                print(f"Warning: {json_filename} is not a valid JSON file. A new file will be created.")

    # 合并旧数据和新数据
    combined_data = existing_data + data

    # 写回JSON文件
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(combined_data, jsonfile, ensure_ascii=False, indent=4)

def save_content_txt(config, content, txt_filename):
    with open(txt_filename, 'a') as f:
        content = '对应题号{}的{}'.format(config['point_id'], config['question_type']) + '\n' + content + '\n\n'
        f.write(content)


async def gen_question(question_config):
    """
    生成题目
    :param point_data:
    :return:
    """

    response = dashscope.Generation.call(
        model='qwen-turbo',
        prompt=question_config['prompt'],
        seed=1234,
        top_p=0.8,
        result_format='message',
        enable_search=False,
        max_tokens=1500,
        temperature=0.85,
        repetition_penalty=1.0
    )

    if response.status_code == HTTPStatus.OK:
        print(response)
        print('\n')
        content = response['output']['choices'][0]['message']['content']
        save_content_txt(question_config, content, '../resources/QA.txt')
        if question_config['question_type'] == '判断题':
            parsed_judge_response(question_config, content)
        elif question_config['question_type'] == '多选题':
            parsed_multi_choice_response(question_config, content)
        else:
            parsed_choice_response(question_config, content)

    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == "__main__":
    asyncio.run(load_data_point(None))
