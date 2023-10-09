import random
from general_utils import *

eg = '''

[开始思考]
任务: 计算6位数除以2位数
题目: 10773/21

除数/被除数=商...余数，余数将*10后给下一位的被除数
从左往右计算：
计算第1位，1/21=0...1
计算第2位，10/21=0...10
计算第3位，107/21=5...2
计算第4位，27/21=1...6
计算第5位，63/21=3...0
计算结果：00513，去掉开头的0后：513
[思考结束]

'''


def make_data_divide(nl, print_all=False, easy=False):
    nls = list(map(str, nl))

    question = make_question(nls, ['/', '/', '除以'])
    print_all and print(question, end='\n\n')

    thinking_lines = [
        '[开始思考]',
        f'任务: 计算{len(nls[0])}位数除以{len(nls[1])}位数',
        f'题目: {"/".join(nls)}',
        '',
        '除数/被除数=商...余数，余数将*10后给下一位的被除数',
        '从左往右计算：'
    ]

    if easy:
        thinking_lines = [
            f'计算{len(nls[0])}位数除以{len(nls[1])}位数',
            '从左往右计算：'
        ]

    jw = 0
    result = ''
    si = 1
    cs = nl[1]
    for i in range(len(nls[0])):
        si = i + 1

        ws = nls[0][i]
        w = int(ws)
        aw = jw * 10 + w
        jw = aw % cs
        c_result = aw // cs
        thinking_lines.append(f'计算第{si}位，{aw}/{cs}={c_result}...{jw}')
        result += str(c_result)

    fl = f'计算结果：{result}'
    if jw != 0:
        fl += f'...{jw}'
    if result[0] == '0':
        result = str(int(result))
        fl += f'，去除开头的0后：{result}'
        if jw != 0:
            fl += f'...{jw}'
    thinking_lines.append(fl)
    if not easy:
        thinking_lines.append('[思考结束]')
    thinking = '\n'.join(thinking_lines)
    print_all and print(thinking, end='\n\n')

    answer = f'{"/".join(nls)}={result}'
    if jw != 0:
        answer += f'...{jw}'
    print_all and print(answer)

    return question, thinking, answer


# make_data_divide([710505, 45], True)
