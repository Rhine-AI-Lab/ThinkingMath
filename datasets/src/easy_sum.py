import random

question_prefix = ['帮我计算一下', '计算', '算下', '求', '']
question_add = ['+', '加']
question_end = ['的结果', '的答案', '']

print_all = False


def random_str(strs):
    return strs[random.randint(0, len(strs) - 1)]


def make_data(nl):
    nls = list(map(str, nl))

    question = random_str(question_prefix) + random_str(question_add).join(nls) + random_str(question_end)
    print_all and print(question, end='\n\n')

    max_len = 0
    for n in nls:
        if len(n) > max_len:
            max_len = len(n)
    thinking_lines = [
        '@THINK{', f'任务: 计算{len(nl)}个数相加，最长是{max_len}位数', f'题目: {"+".join(nls)}', '', '从右往左计算'
    ]

    jw = [0]
    result = ''
    si = 1
    for i in range(max_len):
        si = i + 1
        nl_w = [jw[-1]]
        for ns in nls:
            if len(ns) > i:
                nl_w.append(int(ns[-si]))
            else:
                nl_w.append(0)
        nls_w = list(map(str, nl_w))
        r = sum(nl_w)
        rs = str(r)
        fn = rs[-1]
        line = f'计算第{si}位：{"+".join(nls_w)}={rs}，第{si}位为{fn}'
        if len(rs) == 1:
            jw = [0]
        else:
            # TODO 多位进位合并
            jw = list(map(int, list(rs[:-1])))
            line += f'，进位{rs[:-1]}'
        result = fn + result
        thinking_lines.append(line)

    if len(jw) > 1 or jw[0] > 0:
        jws = ''.join(list(map(str, jw)))
        thinking_lines.append(f'计算第{si + 1}位：来自进位{jws}')
        result = jws + result

    thinking_lines.append('计算结果：' + result)
    thinking_lines += '}'
    thinking = '\n'.join(thinking_lines)
    print_all and print(thinking, end='\n\n')

    answer = "+".join(nls) + '=' + result
    print_all and print(answer)

    return question, thinking, answer


def random_len_int(l):
    return random.randint(10 ** (l - 1), 10 ** l)


tasks = [
    # 数据条数  多少个数字进行相加-随机范围[min, max]  每个数字的位数-随即范围[min, max]
    [20, 2, 2, 2, 3],
    [10, 2, 5, 3, 8],
    [10, 4, 9, 2, 5],
    [10, 2, 3, 6, 15],
]
file = open('../generate/data_example.txt', 'a', encoding='utf-8')

for task in tasks:
    for _ in range(task[0]):
        num = random.randint(task[1], task[2])
        nl = []
        for i in range(num):
            n = random_len_int(random.randint(task[3], task[4]))
            nl.append(n)
        print('Add', nl, '=', sum(nl), end='\n\n')
        question, thinking, answer = make_data(nl)
        file.write(f'{question}\n\n{thinking}\n\n{answer}\n\n\n')
file.close()
