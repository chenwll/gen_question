import re

# 提取问题、答案和解析
content = "1. 判断题：冯·诺依曼体系结构的核心是存储程序概念。\n   答案：正确。\n   解析：冯·诺依曼体系结构（ Von Neumann Architecture）的确将存储程序作为其核心，即计算机的指令和数据都存储在内存中，由CPU按照预先设定的指令顺序执行。\n\n2. 判断题：冯·诺依曼体系结构中，CPU和内存是分开的，数据和指令可以同时存放在内存中。\n   答案：正确。\n   解析：冯·诺依曼结构中，数据和指令都以二进制形式存储在RAM（随机存取内存）中，使得CPU能同时访问两者。\n\n3. 判断题：冯·诺依曼体系结构的计算机只能处理数字，不能处理文字和图形。\n   答案：错误。\n   解析：冯·诺依曼体系结构的计算机可以处理任何数据，包括数字、文字、图形等，通过编码和指令集实现各种操作。\n\n4. 判断题：冯·诺依曼体系结构的计算机中，数据的处理顺序是由硬件自动决定的，与编程无关。\n   答案：错误。\n   解析：在冯·诺依曼体系结构中，数据的处理顺序是由程序员通过编写指令序列来决定的，而不是硬件自动决定的。"

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
        "question": question,
        "answer": ans,
        "analysis": analysis,
    }
    data_list.append(data)
print(data_list)