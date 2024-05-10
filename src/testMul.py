import json
import re
# 获取包含所有题目的内容字符串

content =  "题目1：职业道德的主要内容包括：\nA. 诚实守信\nB. 尊重客户\nC. 专业素养\nD. 团队合作\nE. 持续学习\n\n正确答案：ABCD\n解析：职业道德涵盖了职业行为的基本规范，诚实守信体现了对内对外的诚信，尊重客户体现服务态度，专业素养关乎职业技能，团队合作强调协作精神，而持续学习是保持职业竞争力的重要方面。\n\n题目2：以下哪些行为体现了职业道德中的责任与奉献？\nA. 主动承担责任\nB. 追求个人利益最大化\nC. 乐于助人\nD. 遵守工作规定\nE. 积极创新\n\n正确答案：ACD\n解析：责任与奉献强调的是对工作的敬业精神，主动承担责任和遵守工作规定是履行职责，乐于助人体现对同事和他人的关爱，而追求个人利益最大化则与职业道德中的奉献精神相悖。\n\n题目3：职业道德中关于公平公正的内容包括：\nA. 无偏见对待所有客户\nB. 坚持原则，不谋私利\nC. 同等条件下优先考虑关系亲近的人\nD. 公平分配资源\nE. 保护知识产权\n\n正确答案：ABD\n解析：公平公正要求在处理事务时一视同仁，无偏见对待客户，坚持原则，不利用职务之便，公平分配资源是体现公正的重要方面，而优先考虑关系亲近的人则违背了公正原则。\n\n题目4：职业道德的廉洁自律包括：\nA. 避免利益冲突\nB. 不接受贿赂\nC. 保守商业秘密\nD. 严格遵守财务规定\nE. 私下处理工作问题\n\n正确答案：ABCD\n解析：廉洁自律强调在工作中不贪污受贿，避免利益冲突，保护公司资产，严格遵守财务规定，这些都是廉洁从业的要求，私下处理工作问题可能涉及不透明，不符合廉洁原则。\n\n题目5：职业道德中的尊重与合作体现在：\nA. 尊重同事意见\nB. 遵守团队决策\nC. 提倡多元化观点\nD. 避免背后议论\nE. 无视他人专业能力\n\n正确答案：ABCD\n解析：尊重与合作要求尊重同事，尊重他们的意见和专业能力，遵守团队决策，鼓励多元化观点，避免背后议论以维护良好的工作氛围，而无视他人专业能力是违背尊重原则的。"

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
        "question": question,
        "answer": answer,
        "options": options,
        "analysis": analysis,
    }
    data_list.append(data)
print(data_list)