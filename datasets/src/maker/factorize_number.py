import random


# 分解质因数列表
def factorize_number(number):
    factors = []  # 存储质因数的列表
    divisor = 2  # 初始除数

    while number > 1:
        if number % divisor == 0:
            factors.append(divisor)  # 将除数添加到质因数列表中
            number = number // divisor
        else:
            divisor += 1

    return factors


# 随机组合 不可有一方为1
def random_group_factors(factors):
    expect = random.randint(0, len(factors)-1)
    n1 = 1
    n2 = 1
    for i, f in enumerate(factors):
        if expect == i:
            continue
        if random.random() < 0.5:
            n1 *= f
        else:
            n2 *= f
    ef = factors[expect]
    if n1 == 1:
        n1 = ef
    elif n2 == 1:
        n2 = ef
    else:
        if random.random() < 0.5:
            n1 *= ef
        else:
            n2 *= ef
    return n1, n2
