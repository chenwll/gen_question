import re

# 这是从response中提取的文本内容

content = "1. **题目**: 操作系统的主要功能之一是什么？\n A. 数据加密\n B. 程序编译\n C. 资源管理\n D. 网络通信\n\n **答案**: C. 资源管理\n **解析**: 操作系统的核心职责是管理计算机系统的硬件和软件资源，如内存、CPU、磁盘等，以提供给用户和应用程序使用。\n\n2. **题目**: 在操作系统中，进程和线程的主要区别是什么？\n A. 进程在独立的内存空间运行，线程共享同一进程的内存\n B. 线程拥有独立的CPU，进程不共享\n C. 进程可以并发执行，线程不能\n D. 线程更消耗系统资源\n\n **答案**: A. 进程在独立的内存空间运行，线程共享同一进程的内存\n **解析**: 线程是进程的一部分，共享进程的资源，但有自己的执行上下文，而进程有独立的内存空间。\n\n3. **题目**: 操作系统中的虚拟存储技术，主要解决了哪个问题？\n A. 内存不足\n B. 硬件限制\n C. 数据安全\n D. 磁盘空间不足\n\n **答案**: A. 内存不足\n **解析**: 虚拟存储允许操作系统将程序和数据分散在内存和磁盘上，扩展了可用内存空间，解决了内存容量有限的问题。\n\n4. **题目**: 哪个操作系统模型支持多用户同时交互？\n A. 单用户批处理\n B. 分时系统\n C. 实时系统\n D. 分布式系统\n\n **答案**: B. 分时系统\n **解析**: 分时系统允许多个用户同时交互，每个用户感觉像是独占系统资源。\n\n5. **题目**: 操作系统通过什么机制实现对并发进程的调度？\n A. 进程状态\n B. 优先级\n C. 时间片轮转\n D. 以上都是\n\n **答案**: D. 以上都是\n **解析**: 调度机制通常包括进程状态（如就绪、运行、阻塞）、优先级、时间片轮转等，用于决定哪个进程获得CPU执行权。\n\n6. **题目**: 在操作系统中，哪个概念用于描述硬件对程序的透明性？\n A. 内存保护\n B. 虚拟化\n C. 模块化\n D. 层次结构\n\n **答案**: B. 虚拟化\n **解析**: 虚拟化技术使得操作系统能够为应用程序提供抽象的、与硬件无关的接口，提高了硬件的可利用率和程序的移植性。"
# 正则表达式，用于分割问题、选项、答案和解析
question_pattern = re.compile(r'(\d+)\.\s(.+?)(?=\n\n\d+\.|\n{2,}$)', re.DOTALL)
option_pattern = re.compile(r'([ABCD])\.\s+(.+)')

# 分割整个内容到各个问题
questions = question_pattern.findall(content)
answer_pattern = re.compile(r'[\s\S]*\**答案[:：]\s*\**([A-E,\s]+)')
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
        "question": question_block.split('\n')[0],
        "answer": answer,
        "options": options,
        "analysis": analysis,
    }
    json_list.append(data)
print(json_list)