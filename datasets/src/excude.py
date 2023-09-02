import random
from general_utils import *
from easy_plus import make_data_plus

tasks = [
    # 数据条数  多少个数字进行相加-随机范围[min>=2, max<=10]  每个数字的位数-随即范围[min, max]
    [20, 2, 2, 2, 3],
    [10, 2, 5, 3, 8],
    [10, 4, 9, 2, 5],
    [10, 2, 3, 6, 15],
]
file = open('../generate/data_example.txt', 'w', encoding='utf-8')

data_sep = '================================'

for task in tasks:
    for _ in range(task[0]):
        num = random.randint(task[1], task[2])
        nl = []
        for i in range(num):
            n = random_len_int(random.randint(task[3], task[4]))
            nl.append(n)
        print('Add', nl, '=', sum(nl), end='\n\n')
        g_question, g_thinking, g_answer = make_data_plus(nl)
        file.write(f'{g_question}\n\n{g_thinking}\n\n{g_answer}\n\n{data_sep}\n\n')

file.close()
