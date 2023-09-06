from jsonlines import jsonlines

from maker.general_utils import *
from maker.easy_plus import make_data_plus
from maker.easy_minus import make_data_minus
from maker.easy_times import make_data_times
from maker.easy_divide import make_data_divide

"""
位数：每个数值的长度 随机范围 左右闭区间
同时运算量：同时对多少个数一起计算 当前仅加法支持 随机范围 左右闭区间

# 13b 初步训练 12000条 EPOCH:3
EASY 10000
NORMAL 2000
HARD 1000
"""

PB = {
    'PLUS-1': {
        'rate': 0.12766,

        'EASY': ['PLUS', 0, 2, 4, 2, 3],
        'NORMAL': ['PLUS', 0, 3, 6, 2, 4],
        'HARD': ['PLUS', 0, 4, 8, 2, 5],
    },
    'PLUS-2': {
        'rate': 0.08511,

        'EASY': ['PLUS', 0, 2, 5, 2, 2],
        'NORMAL': ['PLUS', 0, 3, 9, 2, 2],
        'HARD': ['PLUS', 0, 4, 9, 2, 3],
    },
    'PLUS-3': {
        'rate': 0.08511,

        'EASY': ['PLUS', 0, 2, 3, 2, 4],
        'NORMAL': ['PLUS', 0, 3, 5, 3, 6],
        'HARD': ['PLUS', 0, 4, 7, 3, 8],
    },
    'MINUS': {
        'rate': 0.31915,

        'EASY': ['MINUS', 0, 2, 4],
        'NORMAL': ['MINUS', 0, 3, 6],
        'HARD': ['MINUS', 0, 4, 8],
    },
    'TIMES': {
        'rate': 0.19149,

        'EASY': ['TIMES', 0, 1, 3],
        'NORMAL': ['TIMES', 0, 1, 4],
        'HARD': ['TIMES', 0, 1, 7],
    },
    'DIVIDE': {
        'rate': 0.19149,

        'EASY': ['DIVIDE', 0, 1, 3],
        'NORMAL': ['DIVIDE', 0, 1, 4],
        'HARD': ['DIVIDE', 0, 1, 7],
    },
}

ALL = {
    'EASY': 8000,
    'NORMAL': 4000,
    'HARD': 3000,
}

tasks = []
for k, v in ALL.items():
    for _, pbv in PB.items():
        pbv[k][1] = round(pbv['rate'] * v)
        tasks.append(pbv[k])
print('Tasks:')
print('\n'.join(list(map(str, tasks))), '\n')

data_sep = '================================'

print('Expression:')
data = []
for task in tasks:
    for _ in range(task[1]):
        g_question, g_thinking, g_answer = "", "", ""
        if task[0] == 'PLUS':
            num = random.randint(task[4], task[5])
            nl = []
            for i in range(num):
                n = random_len_int(random.randint(task[2], task[3]))
                nl.append(n)
            print(task[0], nl, '=', sum(nl), end='\n')
            g_question, g_thinking, g_answer = make_data_plus(nl)
        elif task[0] == 'MINUS':
            n1 = random_len_int(random.randint(task[2], task[3]))
            n2 = random.randint(10 ** (task[2] - 1), n1)
            nl = [n1, n2]
            print(task[0], nl, '=', n1 - n2, end='\n')
            g_question, g_thinking, g_answer = make_data_minus(nl)
        elif task[0] == 'TIMES':
            n1 = random_len_int(random.randint(task[2], task[3]))
            n2 = random_len_int(random.randint(task[2], task[3]))
            nl = [n1, n2]
            print(task[0], nl, '=', n1 * n2, end='\n')
            g_question, g_thinking, g_answer = make_data_times(nl)
        elif task[0] == 'DIVIDE':
            n1 = random_len_int(random.randint(task[2], task[3]))
            n2 = random_len_int(random.randint(task[2], task[3]))
            if random.random() > 0.2:
                n2 = random.randint(10 ** (task[2] - 1), n1)
                if random.random() > 0.2:
                    n1 = n2 * random.randint(1, 100)
            if n2 == 0:
                n2 = 1
            nl = [n1, n2]
            print(task[0], nl, '=', f'{n1 // n2}...{n1 % n2}', end='\n')
            g_question, g_thinking, g_answer = make_data_divide(nl)
        data.append([task[0], g_question, g_thinking, g_answer])

file = open('../generate/data_example.txt', 'w', encoding='utf-8')
jl = jsonlines.open('../generate/think_math_8k4k3k_v1.jsonl', 'w')

instructions = {
    'PLUS': '计算一个数学加法运算，列出完整的思考过程，包括每一位的计算，进位，以及思考过程。'
            '从右边第一位开始，将每个数字的第一位相加，得出的结果，个位作为作为当前位数的运算结果，'
            '其他的部分作为进位，再前面位数的运算中继续相加，以此类推。'
            '最后按照从右往左重新排列得出最终运算结果，并再思考部分结束后，列出含有答案的式子给用户。',
    'MINUS': '计算一个数学减法运算，列出完整的思考过程，包括每一位的计算，进位，以及思考过程。'
             '从右边第一位开始，对应位置上的数字分别相减，如果不够减，则向前面一位借位，在后续运算前面一位时需额外减一，以此类推。'
             '最后按照从右往左重新排列得出最终运算结果，并再思考部分结束后，列出含有答案的式子给用户。',
    'TIMES': '计算一个数学乘法运算，列出完整的思考过程，包括每一位的计算，进位，以及思考过程。'
             '第一个乘数的每一位与第二个乘数的每一位相乘，第一个乘数得出的结果进行数学加法运算，得出最终答案。'
             '最后加法部分运算结果按照从右往左重新排列得出最终运算结果，并再思考部分结束后，列出含有答案的式子给用户。',
    'DIVIDE': '计算一个数学除法运算，列出完整的思考过程，包括每一位的计算，进位，以及思考过程。'
              '从左往右，每一位都除以除数，余数部分乘以10倍留给下一位。'
              '最后加法部分运算结果按照从右往左重新排列得出最终运算结果，并再思考部分结束后，列出含有答案的式子给用户。',
}

print('')
print('Length:', len(data))
print('Shuffling...')
random.shuffle(data)
print('Writing...')
for line in data:
    file.write(f'{line[0]}\n\n{line[1]}\n\n{line[2]}\n\n{data_sep}\n\n')
    jl.write({'instruction': instructions[line[0]], 'input': line[1], 'output': line[2] + '\n\n' + line[3]})
file.close()
print('Done.')
