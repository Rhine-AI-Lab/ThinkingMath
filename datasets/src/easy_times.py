import random
from general_utils import *
from easy_plus import *


def make_data_times(nl, print_all=False):
    nls = list(map(str, nl))

    question = make_question(nls, ['*', '*', 'x', '乘', '×'])
    print_all and print(question, end='\n\n')

    thinking_lines = [
        '[开始思考]',
        f'任务: 计算{len(nls[0])}位数乘以{len(nls[1])}位数',
        f'题目: {"*".join(nls)}',
        '',
        '第一个数的每一位分别与第二个数的每一位相乘并累加',
    ]

    if nl[0] > nl[1]:
        thinking_lines.append(f'{nl[0]}>{nl[1]}，交换位置：{nl[1]}*{nl[0]}')
        nl[0], nl[1] = nl[1], nl[0]
        nls = list(map(str, nl))

    thinking_lines.append('从右往左计算:')

    result = []
    for i in range(len(nls[0])):
        jw = 0
        cs = int(nls[0][-i - 1])
        thinking_lines.append(f'\n计算乘数第{i + 1}位：{cs}*{nls[1]}*{10 ** i}')
        c_result = ''
        j = 0
        for j in range(len(nls[1])):
            bcs = int(nls[1][-j - 1])
            ir = str(cs * bcs)
            wr = int(ir[-1]) + jw
            c_result = str(wr) + c_result
            line = f'乘第{j + 1}位：{cs}*{bcs}={ir}，第{j + 1}位为{ir[-1]}+{jw}={wr}'
            if len(ir) > 1:
                line += '，进位' + ir[-2]
                jw = int(ir[-2])
            else:
                jw = 0
            thinking_lines.append(line)
        if jw > 0:
            c_result = str(jw) + c_result
            thinking_lines.append(f'仍有进位，第{j}位为：{jw}')
        fcr = int(c_result) * (10 ** i)
        result.append(fcr)
        thinking_lines.append(f'第{i + 1}位结果：{c_result}，{c_result}*{10 ** i}={fcr}')

    thinking_lines.append(f'\n转换为加法任务：' + '+'.join(list(map(str, result))))

    _, think_plus, _ = make_data_plus(result, False)
    think_plus = think_plus.split('从右往左计算:')[1]

    thinking = '\n'.join(thinking_lines) + think_plus
    print_all and print(thinking, end='\n\n')

    answer = "*".join(nls) + '=' + str(sum(result))
    print_all and print(answer)

    return question, thinking, answer


make_data_times([36, 12], True)
