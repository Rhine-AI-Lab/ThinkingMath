import random
from maker.general_utils import *


# 不支持运算结果为负数的情况
def make_data_minus(nl, print_all=False, easy=False):
    nls = list(map(str, nl))

    question = make_question(nls, ['-', '-', '减'])
    print_all and print(question, end='\n\n')

    thinking_lines = [
        '[开始思考]',
        f'任务: 计算{len(nls[0])}位数减去{len(nls[1])}位数',
        f'题目: {"-".join(nls)}',
        '',
        '每一位取对应位置上数字计算 被减数-减数-借位<0 则需要问下一位借位',
        '从右往左计算:'
    ]
    if easy:
        thinking_lines = [
            f'计算{len(nls[0])}位数减去{len(nls[1])}位数',
            '从右往左计算:'
        ]

    jw = [0]
    result = ''
    si = 1
    for i in range(len(nls[0])):
        si = i + 1
        nl_w = []
        for ns in nls:
            if len(ns) > i:
                nl_w.append(int(ns[-si]))
            else:
                nl_w.append(0)
        nls_w = list(map(str, nl_w))

        r = nl_w[0] - nl_w[1] - jw[0]
        sz = f'{nl_w[0]}-{nl_w[1]}-{jw[0]}'
        if r < 0:
            r += 10
            line = f'计算第{si}位：{sz}<0，需要借位。1{sz}={r}，第{si}位为{r}，借位1'
            jw = [1]
        else:
            line = f'计算第{si}位：{sz}>=0，不需要借位。{sz}={r}，第{si}位为{r}'
            jw = [0]
        result = str(r) + result
        thinking_lines.append(line)

    if len(jw) > 1 or jw[0] > 0:
        print('!!!\n计算错误：结果是负数，暂不支持！\n!!!\n')

    fl = f'计算结果：{result}'
    if result[0] == '0':
        result = str(int(result))
        fl += f'，去除开头的0后：{result}'
    thinking_lines.append(fl)
    if not easy:
        thinking_lines.append('[思考结束]')
    thinking = '\n'.join(thinking_lines)
    print_all and print(thinking, end='\n\n')

    answer = "-".join(nls) + '=' + result
    print_all and print(answer)

    return question, thinking, answer
