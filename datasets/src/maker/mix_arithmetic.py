import json
import random
from general_utils import *

eg = """
(((36+(8*(72-4)))/2)+7)
27*[8+(45-3)/6]+10
16*[32+45*(3+6)]/4+9
35+10*(15+32)/2-3
"""

ma_len = 6
operates = ['+', '-', '*', '/']

example = {
    "left": {
        "left": 9,
        "operator": "*",
        "right": {
            "left": 10,
            "operator": "-",
            "right": 4
        }
    },
    "operator": "+",
    "right": 7
}


def is_td(text):
    return text == '*' or text == '/'


def is_pm(text):
    return text == '+' or text == '-'


def is_md(text):
    return text == '-' or text == '/'


# 自定义数值随机生成逻辑
# operator: 运算符  可用于参考生成
def random_number(operator):
    if is_pm(operator):
        return random.randint(10, 10000)
    else:
        return random.randint(10, 100)


def random_layer(target, now_len, level):
    operator = random_str(operates)
    if now_len == 1:
        return random_number(operator)

    left_len = random.randint(1, now_len - 1)
    right_len = now_len - left_len

    target['level'] = level
    target['left'] = random_layer({}, left_len, level + 1)
    target['operator'] = operator
    target['right'] = random_layer({}, right_len, level + 1)

    left_result = target['left'] if left_len == 1 else target['left']['result']
    right_result = target['right'] if right_len == 1 else target['right']['result']
    target['result'] = eval(f'{left_result}{target["operator"]}{right_result}')

    left_expression = target['left'] if left_len == 1 else target['left']['expression']
    right_expression = target['right'] if right_len == 1 else target['right']['expression']

    if is_td(operator):
        if left_len > 1 and is_pm(target['left']['operator']):
            left_expression = f'({left_expression})'
        if right_len > 1 and is_pm(target['right']['operator']):
            right_expression = f'({right_expression})'
    if right_len > 1 and is_pm(target['right']['operator']):
        if is_md(operator) and right_expression[0] != '(':
            right_expression = f'({right_expression})'

    target['expression'] = f'{left_expression} {target["operator"]} {right_expression}'

    return target


expression = random_layer({}, ma_len, 0)
print(json.dumps(expression, indent=4))
print(f'\n{expression["expression"]} = {expression["result"]}\n')

