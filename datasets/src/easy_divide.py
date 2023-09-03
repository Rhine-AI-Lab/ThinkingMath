import random
from general_utils import *

eg = '''

[开始思考]
任务: 计算6位数除以2位数
题目: 10773/21

除数/被除数=商...余数，余数将*10后给下一位的被除数
从左往右计算：
取第1位，1/21=0...1
取第2位，10/21=0...10
取第3位，107/21=5...2
取第4位，27/21=1...6
取第5位，63/21=3...0
计算结果：00513，去掉开头的0后：513
[思考结束]

'''

def make_data_divide(nl, print_all=False):
    nls = list(map(str, nl))

    question = make_question(nls, ['/', '除以'])
    print_all and print(question, end='\n\n')

    thinking_lines = [
        '[开始思考]',
        f'任务: 计算{len(nls[0])}位数减去{len(nls[1])}位数',
        f'题目: {"-".join(nls)}',
        '',
        '每一位取对应位置上数字计算 被减数-减数-借位<0 则需要问下一位借位',
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
    thinking_lines.append('[思考结束]')
    thinking = '\n'.join(thinking_lines)
    print_all and print(thinking, end='\n\n')

    answer = "-".join(nls) + '=' + result
    print_all and print(answer)

    return question, thinking, answer
