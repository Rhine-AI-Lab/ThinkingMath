import random


# 随机从字符串列表中取一个字符串
def random_str(strs):
    return strs[random.randint(0, len(strs) - 1)]


# 随机一个长度的整数
def random_len_int(l):
    return random.randint(10 ** (l - 1), 10 ** l)
