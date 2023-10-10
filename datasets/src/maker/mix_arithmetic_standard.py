import json
import random
from maker.general_utils import *
from maker.factorize_number import *
from maker.easy_plus import make_data_plus
from maker.easy_minus import make_data_minus
from maker.easy_times import make_data_times
from maker.easy_divide import make_data_divide

operates = ['+', '-', '+', '-', '*', '/']  # 数量越多概率越大
use_space = True
use_bracket_level = True


def add_bracket(text, level=0):
    if level == 0:
        text = f'({text})'
    elif level == 1:
        text = f'[{text}]'
    else:
        text = '{' + text + '}'
    return text


# 从外向里递归 初步生成数据及运算符
def random_layer(tree, now_len, level, result):
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

    tree['len'] = now_len
    left_len = random.randint(1, now_len - 1)
    right_len = now_len - left_len

    tree['level'] = level
    # bracket_level = 0
    if left_len == 1:
        tree['left'] = left_result
    else:
        tree['left'] = random_layer({}, left_len, level + 1, left_result)
        # bracket_level = max(target['left']['bracket_level'], bracket_level)
    tree['operator'] = operator
    if right_len == 1:
        tree['right'] = right_result
    else:
        tree['right'] = random_layer({}, right_len, level + 1, right_result)
        # bracket_level = max(target['right']['bracket_level'], bracket_level)
    tree['result'] = result

    # left_expression = target['left'] if left_len == 1 else target['left']['expression']
    # right_expression = target['right'] if right_len == 1 else target['right']['expression']
    # left_tree_expression = target['left'] if left_len == 1 else '(' + target['left']['tree_expression'] + ')'
    # right_tree_expression = target['right'] if right_len == 1 else '(' + target['right']['tree_expression'] + ')'
    # left_math_expression = target['left'] if left_len == 1 else target['left']['math_expression']
    # right_math_expression = target['right'] if right_len == 1 else target['right']['math_expression']

    # had_add_bracket = False
    # if is_td(operator):
    #     if left_len > 1 and is_pm(target['left']['operator']):
    #         left_math_expression = add_bracket(left_expression, bracket_level)
    #         left_expression = f'({left_expression})'
    #         had_add_bracket = True
    #     if right_len > 1 and is_pm(target['right']['operator']):
    #         right_expression = f'({right_expression})'
    #         right_math_expression = add_bracket(right_expression, bracket_level)
    #         had_add_bracket = True
    # if right_len > 1 and is_pm(target['right']['operator']):
    #     if is_md(operator) and right_expression[0] != '(':
    #         right_expression = f'({right_expression})'
    #         right_math_expression = add_bracket(right_expression, bracket_level)
    #         had_add_bracket = True
    # if had_add_bracket:
    #     bracket_level += 1

    # target['expression'] = f'{left_expression} {target["operator"]} {right_expression}'
    # target['tree_expression'] = f'{left_tree_expression} {target["operator"]} {right_tree_expression}'
    # target['math_expression'] = f'{left_math_expression} {target["operator"]} {right_math_expression}'
    # target['bracket_level'] = bracket_level

    return tree


def trans_tree(tree):
    new_left = {
        'left': tree['left'],
        'operator': tree['operator'],
        'right': tree['right']['left'],
    }
    left_len = 1 if is_num(new_left['left']) else new_left['left']['len']
    right_len = 1 if is_num(new_left['right']) else new_left['right']['len']
    new_left['len'] = left_len + right_len
    new_right = tree['right']['right']
    tree['left'] = new_left
    tree['operator'] = tree['right']['operator']
    tree['right'] = new_right
    return tree


def arrange_tree(tree):
    left = tree['left']
    right = tree['right']

    n = 0
    if not is_num(left):
        n += arrange_tree(left)
    if not is_num(right):
        n += arrange_tree(right)

    # print(json.dumps(tree, indent=4))
    if tree['len'] > 2 and not is_num(right):
        if tree['operator'] == '*' and is_td(right['operator']):
            trans_tree(tree)
            n += 1
        if tree['operator'] == '+' and is_pm(right['operator']):
            trans_tree(tree)
            n += 1
    return n


def mark_tree(tree, level=0):
    left = tree['left']
    right = tree['right']
    operator = tree['operator']

    lg = not is_num(left)  # left is group
    rg = not is_num(right)  # right is group

    if lg:
        if mark_tree(left, level=level+1):
            return True
    if rg:
        if mark_tree(right, level=level+1):
            return True

    left_result = left['result'] if lg else left
    left_expression = left['expression'] if lg else left
    left_tree_expression = f"({left['tree_expression']})" if lg else left
    left_math_expression = left['math_expression'] if lg else left
    right_result = right['result'] if rg else right
    right_expression = right['expression'] if rg else right
    right_tree_expression = f"({right['tree_expression']})" if rg else right
    right_math_expression = right['math_expression'] if rg else right

    bracket_level = 0
    if lg:
        bracket_level = max(left['bracket_level'], bracket_level)
    if rg:
        bracket_level = max(right['bracket_level'], bracket_level)

    left_need_bracket = False
    right_need_bracket = False
    if is_td(operator):
        if lg and is_pm(left['operator']):
            left_need_bracket = True
        if rg and is_pm(right['operator']):
            right_need_bracket = True
    if operator == '-':
        if rg and is_pm(right['operator']):
            right_need_bracket = True
    if operator == '/':
        if rg and is_td(right['operator']):
            right_need_bracket = True

    if left_need_bracket:
        left_math_expression = add_bracket(left_math_expression, left['bracket_level'])
        left_expression = f'({left_expression})'
        left['had_bracket'] = True
        bracket_level = max(left['bracket_level'] + 1, bracket_level)
    if right_need_bracket:
        right_math_expression = add_bracket(right_math_expression, right['bracket_level'])
        right_expression = f'({right_expression})'
        right['had_bracket'] = True
        bracket_level = max(right['bracket_level'] + 1, bracket_level)

    tree['level'] = level
    tree['bracket_level'] = bracket_level
    tree['had_bracket'] = False
    result = eval(f'{left_result}{operator}{right_result}')
    if result % 1 != 0:
        return True
    if result < 0:
        return True
    result = int(result)
    tree['result'] = result
    tree['expression'] = f'{left_expression} {tree["operator"]} {right_expression}'
    tree['tree_expression'] = f'{left_tree_expression} {tree["operator"]} {right_tree_expression}'
    tree['math_expression'] = f'{left_math_expression} {tree["operator"]} {right_math_expression}'

    return False


def speak_process(target, i, steps):
    left = target['left']
    right = target['right']
    operator = target['operator']

    lg = not is_num(left)  # left is group
    rg = not is_num(right)  # right is group

    lv = left["result"] if lg else left
    rv = right["result"] if rg else right

    if lg:
        text = speak_process(left, i, steps)
        if 'done' in left and left['done']:
            target['left'] = int(left['result'])
        if text != "":
            return text
    if rg:
        text = speak_process(right, i, steps)
        if 'done' in right and right['done']:
            target['right'] = int(right['result'])
        if text != "":
            return text

    if not lg and not rg:
        text = '然后计算'
        if i == 0:
            text = '先计算'
        elif i == steps - 1:
            text = '最后计算'
        text += f' {lv} {operator} {rv}\n'
        if operator == '+':
            question, thinking, answer = make_data_plus([lv, rv], easy=True)
        elif operator == '-':
            question, thinking, answer = make_data_minus([lv, rv], easy=True)
        elif operator == '*':
            question, thinking, answer = make_data_times([lv, rv], easy=True)
        else:
            question, thinking, answer = make_data_divide([lv, rv], easy=True)
        text += f'\n{thinking}\n\n'
        target["done"] = True
        return text
    return ""


def make_data_mix(length, result, printAll=False):
    tree = random_layer({}, length, 0, result)
    if mark_tree(tree):
        return '', '', -1
    if printAll:
        print(json.dumps(tree, indent=4))
        print('\n-----------------------------------------\n')
        # print(f'{tree["expression"]} = {tree["result"]}')
        print(f'Preliminary order:  {tree["tree_expression"]} = {tree["result"]}')
        print('\n-----------------------------------------\n')
    for i in range(length):
        n = arrange_tree(tree)
        if printAll:
            print(f'Arrange tree: index {i} change {n}')
        if n <= 0:
            break
    mark_tree(tree)
    if printAll:
        print('\n-----------------------------------------\n')
        # print(f'{tree["expression"]} = {tree["result"]}')
        print(f'Operation order:  {tree["tree_expression"]} = {tree["result"]}')
        print(f'Math expression:  {tree["math_expression"]} = {tree["result"]}')
        print('\n')
        print(f'Program:  {tree["expression"]} = {tree["result"]}')
        print(f'Check result:  {eval(tree["expression"])}  {eval(tree["tree_expression"])}  {tree["result"]}  {result}')
        print('\n-----------------------------------------\n')
    result = ""
    steps = tree['len'] - 1
    source_expression = tree["math_expression"]
    cal_result = tree["result"]
    for i in range(steps):
        if i < steps - 1:
            result += f'当前的算式 {tree["math_expression"]}\n'
        result += speak_process(tree, i, steps)
        mark_tree(tree)
    result += f'最终结果：{source_expression} = {tree["result"]}'
    if printAll:
        print(result)
    return source_expression, result, cal_result

# make_data_mix(6, 60, True)
