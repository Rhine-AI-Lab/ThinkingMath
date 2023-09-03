import random


# 随机从字符串列表中取一个字符串
def random_str(strs):
    return strs[random.randint(0, len(strs) - 1)]


def make_question(nls, seps):
    question_prefix = ['帮我计算一下', '计算', '算下', '求', '算', '']
    question_end = ['的结果', '的答案', '']
    question = random_str(question_prefix) + random_str(seps).join(nls) + random_str(question_end)
    return question


# 随机一个长度的整数
def random_len_int(l):
    return random.randint(10 ** (l - 1), 10 ** l)
