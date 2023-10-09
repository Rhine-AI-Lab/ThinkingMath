import json
import random
from general_utils import *
from factorize_number import *

eg = """
(((36+(8*(72-4)))/2)+7)
27*[8+(45-3)/6]+10
16*[32+45*(3+6)]/4+9
35+10*(15+32)/2-3
"""

ma_len = random.randint(5, 8)  # 式子长度
operates = ['+', '-', '+', '-', '*', '/']  # 数量越多概率越大
result = 6666

use_space = True
use_bracket_level = True

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


def add_bracket(text, level=0):
    if level == 0:
        text = f'({text})'
    elif level == 1:
        text = f'[{text}]'
    else:
        text = '{' + text + '}'
    return text


def random_layer(target, now_len, level, result):
    operator = random_str(operates)

    left_result = 0
    right_result = 0
    if operator == '-':
        right_result = random.randint(0, 10000)
        left_result = result + right_result
    elif operator == '*':
        factors = factorize_number(result)
        if len(factors) > 1:
            left_result, right_result = random_group_factors(factors)
        else:
            left_result = 1
            right_result = result
            if random.random() < 0.5:
                left_result, right_result = right_result, left_result
    elif operator == '/':
        right_result = random.randint(1, 100)
        left_result = result * right_result
    else:
        left_result = random.randint(0, result)
        right_result = result - left_result

    left_len = random.randint(1, now_len - 1)
    right_len = now_len - left_len

    target['level'] = level
    bracket_level = 0
    if left_len == 1:
        target['left'] = left_result
    else:
        target['left'] = random_layer({}, left_len, level + 1, left_result)
        bracket_level = max(target['left']['bracket_level'], bracket_level)
    target['operator'] = operator
    if right_len == 1:
        target['right'] = right_result
    else:
        target['right'] = random_layer({}, right_len, level + 1, right_result)
        bracket_level = max(target['right']['bracket_level'], bracket_level)
    target['result'] = result

    left_expression = target['left'] if left_len == 1 else target['left']['expression']
    right_expression = target['right'] if right_len == 1 else target['right']['expression']
    left_tree_expression = target['left'] if left_len == 1 else '(' + target['left']['tree_expression'] + ')'
    right_tree_expression = target['right'] if right_len == 1 else '(' + target['right']['tree_expression'] + ')'
    left_math_expression = target['left'] if left_len == 1 else target['left']['math_expression']
    right_math_expression = target['right'] if right_len == 1 else target['right']['math_expression']

    had_add_bracket = False
    if is_td(operator):
        if left_len > 1 and is_pm(target['left']['operator']):
            left_math_expression = add_bracket(left_expression, bracket_level)
            left_expression = f'({left_expression})'
            had_add_bracket = True
        if right_len > 1 and is_pm(target['right']['operator']):
            right_expression = f'({right_expression})'
            right_math_expression = add_bracket(right_expression, bracket_level)
            had_add_bracket = True
    if right_len > 1 and is_pm(target['right']['operator']):
        if is_md(operator) and right_expression[0] != '(':
            right_expression = f'({right_expression})'
            right_math_expression = add_bracket(right_expression, bracket_level)
            had_add_bracket = True
    if had_add_bracket:
        bracket_level += 1

    target['expression'] = f'{left_expression} {target["operator"]} {right_expression}'
    target['tree_expression'] = f'{left_tree_expression} {target["operator"]} {right_tree_expression}'
    target['math_expression'] = f'{left_math_expression} {target["operator"]} {right_math_expression}'
    target['bracket_level'] = bracket_level

    return target


tree = random_layer({}, ma_len, 0, result)
print(json.dumps(tree, indent=4))

print('\n-----------------------------------------')
print(f'{tree["expression"]} = {tree["result"]}')
print('-----------------------------------------')
