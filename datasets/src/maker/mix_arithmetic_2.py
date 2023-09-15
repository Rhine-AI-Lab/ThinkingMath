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


def random_layer(target, now_len, level):
    if now_len == 1:
        return random.randint(10, 1000)

    left_len = random.randint(1, now_len - 1)
    right_len = now_len - left_len

    target['level'] = level
    target['left'] = random_layer({}, left_len, level + 1)
    target['operator'] = random_str(operates)
    target['right'] = random_layer({}, right_len, level + 1)

    left_result = target['left'] if left_len == 1 else target['left']['result']
    right_result = target['right'] if right_len == 1 else target['right']['result']
    target['result'] = eval(f'{left_result}{target["operator"]}{right_result}')

    return target


expression = random_layer({}, ma_len, 0)
print(json.dumps(expression, indent=4))
