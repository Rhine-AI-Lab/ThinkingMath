import random
from general_utils import *
from easy_plus import make_data_plus
from easy_minus import make_data_minus
from easy_times import make_data_times
from easy_divide import make_data_divide

tasks = [
    # 数据条数    每个数字的位数-随即范围[min, max]    多少个数字进行相加-随机范围[min>=2, max<=10]
    ['PLUS', 20, 2, 2, 2, 3],
    ['PLUS', 10, 2, 5, 3, 8],
    # ['PLUS', 10, 4, 9, 2, 5],
    # ['PLUS', 10, 2, 3, 6, 15],
    ['MINUS', 20, 2, 3],
    ['MINUS', 10, 3, 8],
    ['TIMES', 20, 2, 3],
    ['TIMES', 10, 1, 4],
    ['DIVIDE', 30, 1, 4],
]

data_sep = '================================'


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
            print(task[0], nl, '=', sum(nl), end='\n\n')
            g_question, g_thinking, g_answer = make_data_plus(nl)
        elif task[0] == 'MINUS':
            n1 = random_len_int(random.randint(task[2], task[3]))
            n2 = random.randint(10 ** (task[2] - 1), n1)
            nl = [n1, n2]
            print(task[0], nl, '=', n1 - n2, end='\n\n')
            g_question, g_thinking, g_answer = make_data_minus(nl)
        elif task[0] == 'TIMES':
            n1 = random_len_int(random.randint(task[2], task[3]))
            n2 = random_len_int(random.randint(task[2], task[3]))
            nl = [n1, n2]
            print(task[0], nl, '=', n1 * n2, end='\n\n')
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
            print(task[0], nl, '=', f'{n1 // n2}...{n1 % n2}', end='\n\n')
            g_question, g_thinking, g_answer = make_data_divide(nl)
        data.append([g_question, g_thinking, g_answer])


file = open('../generate/data_example.txt', 'w', encoding='utf-8')
for line in data:
    file.write(f'{line[0]}\n\n{line[1]}\n\n{line[2]}\n\n{data_sep}\n\n')
file.close()
