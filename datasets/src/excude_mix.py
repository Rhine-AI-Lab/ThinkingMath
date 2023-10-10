import random

from jsonlines import jsonlines
import copy

from maker.mix_arithmetic_standard import make_data_mix
from maker.general_utils import *
from maker.easy_plus import make_data_plus
from maker.easy_minus import make_data_minus
from maker.easy_times import make_data_times
from maker.easy_divide import make_data_divide


size = 12000

print('Writing...')
file = open('../generate/data_example.txt', 'w', encoding='utf-8')
jl = jsonlines.open('../generate/think_math_mix_12k_v1.jsonl', 'w')

i = 0
while i < size:
    if i % 500 == 0:
        print(i)
    ti = random.randint(0, 3)
    length = random.randint(4, 8)
    result_truth = random.randint(1000, 4000)
    if ti == 0:
        length = random.randint(3, 5)
        result_truth = random.randint(0, 200)
    elif ti == 1:
        length = random.randint(5, 7)
        result_truth = random.randint(0, 2000)
    elif ti == 2:
        length = random.randint(8, 18)
        result_truth = random.randint(0, 10000)
    equation, output, result = make_data_mix(length, result_truth)
    if len(equation) == 0:
        continue
    file.write(f'{equation} = {result}\n\n{output}\n\n-------------------------------------\n\n')
    jl.write({
        'equation': equation,
        'result': result,
        'type': 'MIX',
        'difficulty': ['EASY', 'NORMAL', 'HARD', 'RANDOM'][ti],
        'length': length,
        'input': equation,
        'output': output,
    })
    i += 1
file.close()
jl.close()

print('Done.')
