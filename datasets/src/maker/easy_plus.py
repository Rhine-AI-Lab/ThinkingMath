import random
from general_utils import *


def make_data_plus(nl, print_all=False):
    nls = list(map(str, nl))

    question = make_question(nls, ['+', '+', '加'])
    print_all and print(question, end='\n\n')

    max_len = 0
    for n in nls:
        if len(n) > max_len:
            max_len = len(n)
    thinking_lines = [
        '[开始思考]',
        f'任务: 计算{len(nl)}个数相加，最长是{max_len}位数',
        f'题目: {"+".join(nls)}',
        '',
        '从右往左计算:'
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
            # TODO 多位进位合并 当前不支持10个以上的数字一起累加进位
            jw = list(map(int, list(rs[:-1])))
            line += f'，进位{rs[:-1]}'
        result = fn + result
        thinking_lines.append(line)

    if len(jw) > 1 or jw[0] > 0:
        jws = ''.join(list(map(str, jw)))
        thinking_lines.append(f'计算第{si + 1}位：来自进位{jws}')
        result = jws + result

    thinking_lines.append('计算结果：' + result)
    thinking_lines.append('[思考结束]')
    thinking = '\n'.join(thinking_lines)
    print_all and print(thinking, end='\n\n')

    answer = "+".join(nls) + '=' + result
    print_all and print(answer)

    return question, thinking, answer

